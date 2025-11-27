
from typing import List
from langchain_community.tools import DuckDuckGoSearchRun

from .models import ResearchState
from .utils import print_section_header, print_progress, truncate_text


class WebSearchTool:
    
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()
    
    def search(self, query: str) -> str:
        """
        
        Args:
            query: The search query
            
        Returns:
            Search results as a string
        """
        try:
            result = self.search_tool.run(query)
            return result
        except Exception as e:
            return f"Error performing search: {str(e)}"
    
    def search_multiple(self, questions: List[str]) -> List[str]:
        """Perform web searches for multiple questions.
        
        Args:
            questions: List of questions to search
            
        Returns:
            List of formatted search results
        """
        search_results = []
        
        print_section_header("🔍 SEARCHING WEB...")
        
        for i, question in enumerate(questions, 1):
            print_progress(f"[{i}/{len(questions)}] Searching: {truncate_text(question)}...")
            
            result = self.search(question)
            search_results.append(
                f"Question: {question}\n\nResults: {result}\n\n"
            )
            
            if result.startswith("Error"):
                print_progress(f"✗ Search failed: {truncate_text(result, 50)}")
            else:
                print_progress(f"✓ Results found ({len(result)} chars)")
        
        print("\n✅ Web search completed")
        return search_results
    
    def search_from_state(self, state: ResearchState) -> ResearchState:
        """Perform web searches using questions from state.
        
        Args:
            state: Current research state
            
        Returns:
            Updated research state with search results
        """
        sub_questions = state["sub_questions"]
        search_results = self.search_multiple(sub_questions)
        state["search_results"] = search_results
        return state
