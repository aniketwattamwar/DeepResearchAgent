
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from .config import Config
from .models import ResearchState
from .nodes import WorkflowNodes
from .search_tool import WebSearchTool


class WorkflowBuilder:
    
    def __init__(
        self,
        model_name: str,
        num_sub_questions: int,
        max_iterations: int,
        question_prompt: str,
        analysis_prompt: str,
        reflection_prompt: str,
        report_prompt: str
    ):
        """
        
        Args:
            model_name: Name of the language model to use
            num_sub_questions: Number of sub-questions to generate
            max_iterations: Maximum reflection iterations
            question_prompt: System prompt for question generation
            analysis_prompt: System prompt for analysis
            reflection_prompt: System prompt for reflection
            report_prompt: System prompt for report generation
        """
        self.model_name = model_name
        self.num_sub_questions = num_sub_questions
        self.max_iterations = max_iterations
        self.question_prompt = question_prompt
        self.analysis_prompt = analysis_prompt
        self.reflection_prompt = reflection_prompt
        self.report_prompt = report_prompt
    
    def build(self):
        """
        
        Returns:
            Compiled workflow graph
        """

        llm = ChatOpenAI(
            model=self.model_name,
            api_key=Config.get_openai_api_key(),
            temperature=Config.DEFAULT_TEMPERATURE
        )
        
        search_tool = WebSearchTool()
        
        nodes = WorkflowNodes(
            llm=llm,
            search_tool=search_tool,
            num_sub_questions=self.num_sub_questions,
            max_iterations=self.max_iterations,
            question_prompt=self.question_prompt,
            analysis_prompt=self.analysis_prompt,
            reflection_prompt=self.reflection_prompt,
            report_prompt=self.report_prompt
        )
        
        workflow = StateGraph(ResearchState)
        
        workflow.add_node("generate_sub_questions", nodes.generate_sub_questions)
        workflow.add_node("search_web", nodes.search_web)
        workflow.add_node("analyze_context", nodes.analyze_context)
        workflow.add_node("generate_report", nodes.generate_report)
        
        workflow.set_entry_point("generate_sub_questions")
        
        workflow.add_edge("generate_sub_questions", "search_web")
        workflow.add_edge("search_web", "analyze_context")
        workflow.add_conditional_edges(
            "analyze_context",
            nodes.reflect_on_analysis,
            {
                "analyze_context": "analyze_context",
                "generate_report": "generate_report"
            }
        )
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    @staticmethod
    def create_initial_state(query: str) -> ResearchState:
        """Create initial state for the workflow.
        
        Args:
            query: Research query
            
        Returns:
            Initial research state
        """
        return {
            "query": query,
            "sub_questions": [],
            "search_results": [],
            "analysis": "",
            "report": "",
            "iteration": 0
        }
