
from typing import Callable
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith.run_helpers import traceable

from .models import ResearchState
from .prompts import Prompts
from .search_tool import WebSearchTool
from .utils import (
    print_section_header,
    print_progress,
    print_numbered_list,
    clean_questions
)


class WorkflowNodes:
    
    def __init__(
        self,
        llm: ChatOpenAI,
        search_tool: WebSearchTool,
        num_sub_questions: int,
        max_iterations: int,
        question_prompt: str,
        analysis_prompt: str,
        reflection_prompt: str,
        report_prompt: str
    ):
        """Initialize workflow nodes.
        
        Args:
            llm: Language model instance
            search_tool: Web search tool instance
            num_sub_questions: Number of sub-questions to generate
            max_iterations: Maximum reflection iterations
            question_prompt: System prompt for question generation
            analysis_prompt: System prompt for analysis
            reflection_prompt: System prompt for reflection
            report_prompt: System prompt for report generation
        """
        self.llm = llm
        self.search_tool = search_tool
        self.num_sub_questions = num_sub_questions
        self.max_iterations = max_iterations
        self.question_prompt = question_prompt
        self.analysis_prompt = analysis_prompt
        self.reflection_prompt = reflection_prompt
        self.report_prompt = report_prompt
    
    @traceable(run_type="chain", name="generate_sub_questions")
    def generate_sub_questions(self, state: ResearchState) -> ResearchState:
        """Generate sub-questions for the research topic.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with sub-questions
        """
        query = state["query"]
        print_section_header("🔵 GENERATING SUB-QUESTIONS...")
        
        prompt = [
            SystemMessage(content=self.question_prompt),
            HumanMessage(content=Prompts.get_question_generation_prompt(
                query, self.num_sub_questions
            ))
        ]
        response = self.llm.invoke(prompt)
        
        questions = clean_questions(
            response.content.strip().split('\n')
        )[:self.num_sub_questions]
        
        # Use default questions if generation failed
        if len(questions) < self.num_sub_questions:
            questions = Prompts.get_default_sub_questions(
                query, self.num_sub_questions
            )
        
        state["sub_questions"] = questions
        state["iteration"] = 0
        
        print("\n✅ Sub-questions generated:")
        print_numbered_list(questions)
        
        return state
    
    @traceable(run_type="tool", name="search_web")
    def search_web(self, state: ResearchState) -> ResearchState:
        """Perform web searches for sub-questions.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with search results
        """
        return self.search_tool.search_from_state(state)
    
    @traceable(run_type="chain", name="analyze_context")
    def analyze_context(self, state: ResearchState) -> ResearchState:
        """Analyze search results and generate insights.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with analysis
        """
        query = state["query"]
        search_results = state["search_results"]
        
        print_section_header(
            f"🧠 ANALYZING RESULTS (Iteration {state['iteration'] + 1})..."
        )
        
        context = "\n\n".join(search_results)
        
        prompt = [
            SystemMessage(content=self.analysis_prompt),
            HumanMessage(content=Prompts.get_analysis_prompt(query, context))
        ]
        
        response = self.llm.invoke(prompt)
        state["analysis"] = response.content
        state["iteration"] += 1
        
        print(f"\n✅ Analysis completed ({len(response.content)} chars)")
        
        return state
    
    def reflect_on_analysis(self, state: ResearchState) -> str:
        """Reflect on analysis quality and decide next step.
        
        Args:
            state: Current research state
            
        Returns:
            Next node name to execute
        """
        analysis = state["analysis"]
        iteration = state["iteration"]
        
        print_section_header("🤔 REFLECTING ON ANALYSIS...")
        
        if iteration >= self.max_iterations:
            print_progress(f"⏱️  Max iterations ({self.max_iterations}) reached")
            print_progress("→ Proceeding to report generation")
            return "generate_report"
        
        prompt = [
            SystemMessage(content=self.reflection_prompt),
            HumanMessage(content=Prompts.get_reflection_prompt(analysis))
        ]
        
        response = self.llm.invoke(prompt)
        
        if "yes" in response.content.lower()[:50]:
            print(response.content.lower())
            print("=" * 60)
            print_progress("✓ Analysis is comprehensive")
            print_progress("→ Proceeding to report generation")
            return "generate_report"
        else:
            print_progress("⚠️  Analysis needs improvement")
            print_progress("→ Re-analyzing with more depth")
            return "analyze_context"
    
    @traceable(run_type="chain", name="generate_report")
    def generate_report(self, state: ResearchState) -> ResearchState:
        """Generate final research report.
        
        Args:
            state: Current research state
            
        Returns:
            Updated state with final report
        """
        query = state["query"]
        analysis = state["analysis"]
        
        print_section_header("📄 GENERATING FINAL REPORT...")
        
        prompt = [
            SystemMessage(content=self.report_prompt),
            HumanMessage(content=Prompts.get_report_generation_prompt(
                query, analysis
            ))
        ]
        
        response = self.llm.invoke(prompt)
        state["report"] = response.content
        
        print(f"\n✅ Report generated ({len(response.content)} chars)")
        
        return state
