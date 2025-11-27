from .config import Config
from .prompts import Prompts
from .workflow import WorkflowBuilder
from .utils import (
    print_section_header,
    print_subsection_header,
    print_numbered_list,
    save_report_to_file,
    validate_input_range
)


def get_user_input() -> tuple:
    """ 
    
    Returns:
        Tuple of (query, model_name, num_sub_questions, max_iterations, prompts)
    """
    print_section_header("🔬 DEEP RESEARCH AGENT")
    
    query = input("\n📝 Enter your research topic: ").strip()
    
    if not query:
        raise ValueError("Research topic cannot be empty")
    
    print_subsection_header("⚙️  CONFIGURATION")
    
    # Model selection
    model_input = input(
        "Select model (gpt-4/gpt-4-turbo/gpt-4o/gpt-4o-mini/gpt-3.5-turbo) "
        "[default: gpt-4]: "
    ).strip()
    model_name = model_input if model_input else Config.DEFAULT_MODEL
    
    # Number of sub-questions
    num_questions_input = input(
        f"Number of sub-questions ({Config.MIN_SUB_QUESTIONS}-{Config.MAX_SUB_QUESTIONS}) "
        f"[default: {Config.DEFAULT_NUM_SUB_QUESTIONS}]: "
    ).strip()
    num_sub_questions = validate_input_range(
        num_questions_input,
        Config.MIN_SUB_QUESTIONS,
        Config.MAX_SUB_QUESTIONS,
        Config.DEFAULT_NUM_SUB_QUESTIONS
    )
    
    # Maximum iterations
    max_iter_input = input(
        f"Max reflection iterations ({Config.MIN_ITERATIONS}-{Config.MAX_ITERATIONS}) "
        f"[default: {Config.DEFAULT_MAX_ITERATIONS}]: "
    ).strip()
    max_iterations = validate_input_range(
        max_iter_input,
        Config.MIN_ITERATIONS,
        Config.MAX_ITERATIONS,
        Config.DEFAULT_MAX_ITERATIONS
    )
    
    # Custom prompts
    custom_prompts = input(
        "\nUse custom system prompts? (y/n) [default: n]: "
    ).strip().lower()
    
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
    
    # Use defaults for empty prompts
    prompts = {
        "question_prompt": question_prompt or Prompts.QUESTION_GENERATION,
        "analysis_prompt": analysis_prompt or Prompts.ANALYSIS,
        "reflection_prompt": reflection_prompt or Prompts.REFLECTION,
        "report_prompt": report_prompt or Prompts.REPORT_GENERATION
    }
    
    return query, model_name, num_sub_questions, max_iterations, prompts


def display_configuration(
    model_name: str,
    num_sub_questions: int,
    max_iterations: int,
    custom_prompts: bool
) -> None:
    """Display research configuration.
    
    Args:
        model_name: Name of the model
        num_sub_questions: Number of sub-questions
        max_iterations: Maximum iterations
        custom_prompts: Whether custom prompts are used
    """
    print_section_header("🚀 STARTING RESEARCH WORKFLOW")
    print(f"\n📊 Configuration:")
    print(f"  • Model: {model_name}")
    print(f"  • Sub-questions: {num_sub_questions}")
    print(f"  • Max iterations: {max_iterations}")
    print(f"  • Custom prompts: {'Yes' if custom_prompts else 'No'}")


def display_results(result: dict) -> None:
    """Display research results.
    
    Args:
        result: Research result dictionary
    """
    print_section_header("📊 FINAL RESEARCH REPORT")
    print(f"\n🔍 Query: {result['query']}")
    print(f"\n📋 Sub-Questions:")
    print_numbered_list(result['sub_questions'])
    print(f"\n{'=' * 60}")
    print(result['report'])
    print("=" * 60)


def save_results(
    result: dict,
    model_name: str,
    num_sub_questions: int,
    max_iterations: int
) -> None:
    """Prompt user to save results to file.
    
    Args:
        result: Research result dictionary
        model_name: Name of the model
        num_sub_questions: Number of sub-questions
        max_iterations: Maximum iterations
    """
    save = input("\n💾 Save report to file? (y/n) [default: n]: ").strip().lower()
    
    if save == 'y':
        filename = input(
            "Enter filename [default: research_report.md]: "
        ).strip()
        filename = filename if filename else "research_report.md"
        
        if save_report_to_file(
            filename,
            result['query'],
            result['sub_questions'],
            result['report'],
            model_name,
            num_sub_questions,
            max_iterations
        ):
            print(f"✅ Report saved to {filename}")


def run_research() -> None:
    """Main function to run the research workflow."""
    try:
        # Setup environment
        Config.setup_environment()
        Config.validate_config()
        
        # Get user input
        query, model_name, num_sub_questions, max_iterations, prompts = get_user_input()
        
        # Display configuration
        display_configuration(
            model_name,
            num_sub_questions,
            max_iterations,
            any(prompts.values())
        )
        
        # Build and run workflow
        builder = WorkflowBuilder(
            model_name=model_name,
            num_sub_questions=num_sub_questions,
            max_iterations=max_iterations,
            **prompts
        )
        
        app = builder.build()
        initial_state = builder.create_initial_state(query)
        result = app.invoke(initial_state)
        
        # Display and save results
        display_results(result)
        save_results(result, model_name, num_sub_questions, max_iterations)
        
        print("\n✅ Research completed successfully!")
        
    except ValueError as e:
        print(f"❌ Error: {str(e)}")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_research()
