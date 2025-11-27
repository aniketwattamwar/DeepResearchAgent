"""
Utility functions for the Deep Research Agent.
"""

from typing import List, Optional


def print_section_header(title: str, width: int = 60) -> None:
    """Print a formatted section header.
    
    Args:
        title: The title to display
        width: Width of the separator line
    """
    print(f"\n{'=' * width}")
    print(title)
    print(f"{'=' * width}")


def print_subsection_header(title: str, width: int = 60) -> None:
    """Print a formatted subsection header.
    
    Args:
        title: The title to display
        width: Width of the separator line
    """
    print(f"\n{'-' * width}")
    print(title)
    print(f"{'-' * width}")


def print_progress(message: str, indent: int = 2) -> None:
    """Print a progress message with indentation.
    
    Args:
        message: The message to display
        indent: Number of spaces to indent
    """
    print(f"{' ' * indent}{message}")


def print_numbered_list(items: List[str], indent: int = 2) -> None:
    """Print a numbered list of items.
    
    Args:
        items: List of items to display
        indent: Number of spaces to indent
    """
    for i, item in enumerate(items, 1):
        print(f"{' ' * indent}{i}. {item}")


def save_report_to_file(
    filename: str,
    query: str,
    sub_questions: List[str],
    report: str,
    model_name: str,
    num_sub_questions: int,
    max_iterations: int
) -> bool:
    """ 
    
    Args:
        filename: Name of the file to save
        query: The research query
        sub_questions: List of sub-questions
        report: The generated report
        model_name: Name of the model used
        num_sub_questions: Number of sub-questions
        max_iterations: Maximum iterations used
        
    Returns:
        True if save was successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Research Report\n\n")
            f.write(f"**Query:** {query}\n\n")
            f.write(f"**Configuration:**\n")
            f.write(f"- Model: {model_name}\n")
            f.write(f"- Sub-questions: {num_sub_questions}\n")
            f.write(f"- Max iterations: {max_iterations}\n\n")
            f.write(f"## Sub-Questions\n\n")
            for i, q in enumerate(sub_questions, 1):
                f.write(f"{i}. {q}\n")
            f.write(f"\n## Report\n\n")
            f.write(report)
        return True
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")
        return False


def validate_input_range(
    value: str,
    min_val: int,
    max_val: int,
    default: int
) -> int:
    """Validate and convert input to integer within range.
    
    Args:
        value: Input string to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        default: Default value if input is invalid
        
    Returns:
        Validated integer value
    """
    if not value:
        return default
    
    try:
        num = int(value)
        if min_val <= num <= max_val:
            return num
        else:
            print(f"⚠️  Value out of range. Using default: {default}")
            return default
    except ValueError:
        print(f"⚠️  Invalid input. Using default: {default}")
        return default


def truncate_text(text: str, max_length: int = 60) -> str:
    """Truncate text to maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def clean_questions(questions: List[str], min_length: int = 10) -> List[str]:
    """Clean and filter list of questions.
    
    Args:
        questions: List of raw questions
        min_length: Minimum length for valid questions
        
    Returns:
        Cleaned list of questions
    """
    return [
        q.strip()
        for q in questions
        if q.strip() and len(q.strip()) > min_length
    ]
