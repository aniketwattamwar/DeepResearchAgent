from typing import TypedDict, List, Annotated
import operator


class ResearchState(TypedDict):
    """ 
    
    Attributes:
        query: The main research query
        sub_questions: List of generated sub-questions
        search_results: Accumulated search results
        analysis: Current analysis of search results
        report: Final research report
        iteration: Current iteration count
    """
    query: str
    sub_questions: List[str]
    search_results: Annotated[List[str], operator.add]
    analysis: str
    report: str
    iteration: int
