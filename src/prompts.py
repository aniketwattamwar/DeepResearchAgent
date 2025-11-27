class Prompts:
    """Collection of system prompts for the research workflow."""
    
    QUESTION_GENERATION = (
        "You are an expert research analyst. Generate specific, focused "
        "sub-questions for research topics."
    )
    
    ANALYSIS = (
        "You are an expert research analyst. Analyze the provided search "
        "results and synthesize key insights that directly answer the research query."
    )
    
    REFLECTION = (
        "You are a critical reviewer. Evaluate if the analysis is comprehensive "
        "and well-supported."
    )
    
    REPORT_GENERATION = (
        "You are an expert research report writer. Create well-structured, "
        "comprehensive reports with clear sections and citations."
    )
    
    @staticmethod
    def get_question_generation_prompt(query: str, num_questions: int) -> str:
        """Generate prompt for sub-question generation.
        
        Args:
            query: The main research query
            num_questions: Number of sub-questions to generate
            
        Returns:
            Formatted prompt string
        """
        return f"""Given the research topic: {query}

Generate exactly {num_questions} specific, focused sub-questions that will help thoroughly research this topic. Return only the {num_questions} questions, one per line, without numbering or extra text."""
    
    @staticmethod
    def get_analysis_prompt(query: str, context: str) -> str:
        """Generate prompt for context analysis.
        
        Args:
            query: The main research query
            context: Combined search results
            
        Returns:
            Formatted prompt string
        """
        return f"""Research Query: {query}

Search Results:
{context}

Analyze these search results and provide:
1. Key findings and insights
2. Important patterns or trends
3. Relevant facts and data points
4. Potential gaps or areas needing more research

Provide a comprehensive analysis."""
    
    @staticmethod
    def get_reflection_prompt(analysis: str) -> str:
        """Generate prompt for analysis reflection.
        
        Args:
            analysis: The current analysis to reflect on
            
        Returns:
            Formatted prompt string
        """
        return f"""Analysis:
{analysis}

Is this analysis comprehensive, well-supported, and ready for report generation? Answer with 'yes' or 'no' and briefly explain why."""
    
    @staticmethod
    def get_report_generation_prompt(query: str, analysis: str) -> str:
        """Generate prompt for final report generation.
        
        Args:
            query: The main research query
            analysis: The completed analysis
            
        Returns:
            Formatted prompt string
        """
        return f"""Research Topic: {query}

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
"""
    
    @staticmethod
    def get_default_sub_questions(query: str, num_questions: int) -> list[str]:
        """Generate default sub-questions as fallback.
        
        Args:
            query: The main research query
            num_questions: Number of questions to generate
            
        Returns:
            List of default sub-questions
        """
        default_questions = [
            f"What are the key concepts of {query}?",
            f"What are the current trends and developments in {query}?",
            f"What are the practical applications of {query}?",
            f"What are the challenges and limitations of {query}?",
            f"What is the future outlook for {query}?"
        ]
        return default_questions[:num_questions]
