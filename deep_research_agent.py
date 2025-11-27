import os
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
import operator
from langsmith.run_helpers import traceable

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "" # Add your key
os.environ["LANGCHAIN_PROJECT"] = "default"

openai_api_key = "" # Add your key

class ResearchState(TypedDict):
    query: str
    sub_questions: List[str]
    search_results: Annotated[List[str], operator.add]
    analysis: str
    report: str
    iteration: int

search_tool = DuckDuckGoSearchRun()

def create_workflow(
    model_name,
    num_sub_questions,
    max_iterations,
    question_prompt,
    analysis_prompt,
    reflection_prompt,
    report_prompt
):
    llm = ChatOpenAI(
        model=model_name,
        api_key=openai_api_key,
        temperature=0.7
    )

    @traceable(run_type="chain", name="generate_sub_questions")
    def generate_sub_questions(state: ResearchState) -> ResearchState:
        query = state["query"]
        print(f"\n{'='*60}")
        print("🔵 GENERATING SUB-QUESTIONS...")
        print(f"{'='*60}")
        
        prompt = [
            SystemMessage(content=question_prompt),
            HumanMessage(content=f"""Given the research topic: {query}

Generate exactly {num_sub_questions} specific, focused sub-questions that will help thoroughly research this topic. Return only the {num_sub_questions} questions, one per line, without numbering or extra text.""")
        ]
        response = llm.invoke(prompt)
        
        questions = [q.strip() for q in response.content.strip().split('\n') if q.strip() and len(q.strip()) > 10][:num_sub_questions]
        
        if len(questions) < num_sub_questions:
            default_questions = [
                f"What are the key concepts of {query}?",
                f"What are the current trends and developments in {query}?",
                f"What are the practical applications of {query}?",
                f"What are the challenges and limitations of {query}?",
                f"What is the future outlook for {query}?"
            ]
            questions = default_questions[:num_sub_questions]
        
        state["sub_questions"] = questions
        state["iteration"] = 0
        
        print("\n✅ Sub-questions generated:")
        for i, q in enumerate(questions, 1):
            print(f"  {i}. {q}")
        
        return state

    @traceable(run_type="tool", name="search_web")
    def search_web(state: ResearchState) -> ResearchState:
        sub_questions = state["sub_questions"]
        search_results = []
        
        print(f"\n{'='*60}")
        print("🔍 SEARCHING WEB...")
        print(f"{'='*60}")
        
        for i, question in enumerate(sub_questions, 1):
            print(f"\n  [{i}/{len(sub_questions)}] Searching: {question[:60]}...")
            try:
                result = search_tool.run(question)
                search_results.append(f"Question: {question}\n\nResults: {result}\n\n")
                print(f"  ✓ Results found ({len(result)} chars)")
            except Exception as e:
                search_results.append(f"Question: {question}\n\nResults: Error performing search - {str(e)}\n\n")
                print(f"  ✗ Search failed: {str(e)[:50]}")
        
        state["search_results"] = search_results
        print("\n✅ Web search completed")
        
        return state

    @traceable(run_type="chain", name="analyze_context")
    def analyze_context(state: ResearchState) -> ResearchState:
        query = state["query"]
        search_results = state["search_results"]
        
        print(f"\n{'='*60}")
        print(f"🧠 ANALYZING RESULTS (Iteration {state['iteration'] + 1})...")
        print(f"{'='*60}")
        
        context = "\n\n".join(search_results)
        
        prompt = [
            SystemMessage(content=analysis_prompt),
            HumanMessage(content=f"""Research Query: {query}

Search Results:
{context}

Analyze these search results and provide:
1. Key findings and insights
2. Important patterns or trends
3. Relevant facts and data points
4. Potential gaps or areas needing more research

Provide a comprehensive analysis.""")
        ]
        
        response = llm.invoke(prompt)
        state["analysis"] = response.content
        state["iteration"] += 1
        
        print(f"\n✅ Analysis completed ({len(response.content)} chars)")
        
        return state

    def reflect_on_analysis(state: ResearchState) -> str:
        analysis = state["analysis"]
        iteration = state["iteration"]
        
        print(f"\n{'='*60}")
        print("🤔 REFLECTING ON ANALYSIS...")
        print(f"{'='*60}")
        
        if iteration >= max_iterations:
            print(f"  ⏱️  Max iterations ({max_iterations}) reached")
            print("  → Proceeding to report generation")
            return "generate_report"
        
        prompt = [
            SystemMessage(content=reflection_prompt),
            HumanMessage(content=f"""Analysis:
{analysis}

Is this analysis comprehensive, well-supported, and ready for report generation? Answer with 'yes' or 'no' and briefly explain why.""")
        ]
        
        response = llm.invoke(prompt)
        
        if "yes" in response.content.lower()[:50]:
            print(response.content.lower())
            print(f"{'='*60}")
            print("  ✓ Analysis is comprehensive")
            print("  → Proceeding to report generation")
             
            return "generate_report"
        else:
            print("  ⚠️  Analysis needs improvement")
            print("  → Re-analyzing with more depth")
            return "analyze_context"

    @traceable(run_type="chain", name="generate_report")
    def generate_report(state: ResearchState) -> ResearchState:
        query = state["query"]
        analysis = state["analysis"]
        
        print(f"\n{'='*60}")
        print("📄 GENERATING FINAL REPORT...")
        print(f"{'='*60}")
        
        prompt = [
            SystemMessage(content=report_prompt),
            HumanMessage(content=f"""Research Topic: {query}

Analysis:
{analysis}

Create a comprehensive research report with the following structure:
1. Executive Summary: Synthesize the main conclusion and the top three key findings into a single, concise paragraph. Focus on actionable insights, not just facts.
2. Introduction: Define the scope of the research (the original user query). State the methodology used (e.g., "Iterative search across web and academic sources using a Multi-Agent system"). Define the sub-questions addressed.
3. Key Findings: Present the answers to the sub-questions as numbered or bulleted claims. Every claim must be immediately followed by an inline citation
4. Detailed Analysis: This section must demonstrate synthesis and reasoning. Do not simply list facts. Instead, compare and contrast conflicting sources, analyze trends, and discuss the implications of the Key Findings
5. Conclusions and Recommendations: Restate the primary conclusion. Offer 2-3 forward-looking recommendations based on the analysis (e.g., "Further research is recommended on...") or suggest a business strategy. Provide all sources as well.

Make it informative, well-organized, and professional.
Include a short summary of the steps taken (Planner's sub-questions, Reflection loops, Confidence Score)
""")
        ]
        
        response = llm.invoke(prompt)
        state["report"] = response.content
        
        print(f"\n✅ Report generated ({len(response.content)} chars)")
        
        return state
    
    workflow = StateGraph(ResearchState)
    workflow.add_node("generate_sub_questions", generate_sub_questions)
    workflow.add_node("search_web", search_web)
    workflow.add_node("analyze_context", analyze_context)
    workflow.add_node("generate_report", generate_report)
    workflow.set_entry_point("generate_sub_questions")
    workflow.add_edge("generate_sub_questions", "search_web")
    workflow.add_edge("search_web", "analyze_context")
    workflow.add_conditional_edges(
        "analyze_context",
        reflect_on_analysis,
        {
            "analyze_context": "analyze_context",
            "generate_report": "generate_report"
        }
    )
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()


def run_research():
    print("\n" + "="*60)
    print("🔬 DEEP RESEARCH AGENT")
    print("="*60)
    
    query = input("\n📝 Enter your research topic: ").strip()
    
    if not query:
        print("❌ Error: Research topic cannot be empty")
        return
    
    print("\n" + "-"*60)
    print("⚙️  CONFIGURATION")
    print("-"*60)
    
    model_input = input("Select model (gpt-4/gpt-4-turbo/gpt-4o/gpt-4o-mini/gpt-3.5-turbo) [default: gpt-4]: ").strip()
    model_name = model_input if model_input else "gpt-4"
    
    num_questions_input = input("Number of sub-questions (1-10) [default: 3]: ").strip()
    num_sub_questions = int(num_questions_input) if num_questions_input.isdigit() else 3
    
    max_iter_input = input("Max reflection iterations (1-5) [default: 2]: ").strip()
    max_iterations = int(max_iter_input) if max_iter_input.isdigit() else 2
    
    custom_prompts = input("\nUse custom system prompts? (y/n) [default: n]: ").strip().lower()
    
    if custom_prompts == 'y':
        print("\n📋 Custom Prompts (press Enter to use default):")
        question_prompt = input("Question generation prompt: ").strip()
        analysis_prompt = input("Analysis prompt: ").strip()
        reflection_prompt = input("Reflection prompt: ").strip()
        report_prompt = input("Report generation prompt: ").strip()
    else:
        question_prompt = ""
        analysis_prompt = ""
        reflection_prompt = ""
        report_prompt = ""
    
    question_prompt = question_prompt or "You are an expert research analyst. Generate specific, focused sub-questions for research topics."
    analysis_prompt = analysis_prompt or "You are an expert research analyst. Analyze the provided search results and synthesize key insights that directly answer the research query."
    reflection_prompt = reflection_prompt or "You are a critical reviewer. Evaluate if the analysis is comprehensive and well-supported."
    report_prompt = report_prompt or "You are an expert research report writer. Create well-structured, comprehensive reports with clear sections and citations."
    
    print("\n" + "="*60)
    print("🚀 STARTING RESEARCH WORKFLOW")
    print("="*60)
    print(f"\n📊 Configuration:")
    print(f"  • Model: {model_name}")
    print(f"  • Sub-questions: {num_sub_questions}")
    print(f"  • Max iterations: {max_iterations}")
    print(f"  • Custom prompts: {'Yes' if custom_prompts == 'y' else 'No'}")
    
    try:
        app = create_workflow(
            model_name,
            num_sub_questions,
            max_iterations,
            question_prompt,
            analysis_prompt,
            reflection_prompt,
            report_prompt
        )
        
        initial_state = {
            "query": query,
            "sub_questions": [],
            "search_results": [],
            "analysis": "",
            "report": "",
            "iteration": 0
        }
        
        result = app.invoke(initial_state)
        
        print("\n" + "="*60)
        print("📊 FINAL RESEARCH REPORT")
        print("="*60)
        print(f"\n🔍 Query: {result['query']}")
        print(f"\n📋 Sub-Questions:")
        for i, q in enumerate(result['sub_questions'], 1):
            print(f"  {i}. {q}")
        print(f"\n{'='*60}")
        print(result['report'])
        print("="*60)
        
        save = input("\n💾 Save report to file? (y/n) [default: n]: ").strip().lower()
        if save == 'y':
            filename = input("Enter filename [default: research_report.md]: ").strip()
            filename = filename if filename else "research_report.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Research Report\n\n")
                f.write(f"**Query:** {result['query']}\n\n")
                f.write(f"**Configuration:**\n")
                f.write(f"- Model: {model_name}\n")
                f.write(f"- Sub-questions: {num_sub_questions}\n")
                f.write(f"- Max iterations: {max_iterations}\n\n")
                f.write(f"## Sub-Questions\n\n")
                for i, q in enumerate(result['sub_questions'], 1):
                    f.write(f"{i}. {q}\n")
                f.write(f"\n## Report\n\n")
                f.write(result['report'])
            
            print(f"✅ Report saved to {filename}")
        
        print("\n✅ Research completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_research()