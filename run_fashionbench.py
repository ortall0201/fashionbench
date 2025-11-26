#!/usr/bin/env python3
"""
FashionBench - Fashion Industry LLM Evaluation Suite

Main runner script for executing all FashionBench evaluations.
Provides a command-line interface for running individual or all evaluations.

Usage:
    python run_fashionbench.py --model claude-3-sonnet
    python run_fashionbench.py --model gpt-4 --eval trend_detection
    python run_fashionbench.py --model simulated --verbose
"""

import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from typing import Optional

# Import all evaluation modules
from evals.trend_detection_eval import evaluate_trend_detection
from evals.product_extraction_eval import evaluate_product_extraction
from evals.style_eval import evaluate_style_classification
from evals.writing_eval import evaluate_fashion_writing
from evals.hashtag_eval import evaluate_hashtag_understanding
from evals.affiliate_eval import evaluate_affiliate_detection

# Initialize Rich console for beautiful output
console = Console()
app = typer.Typer(help="FashionBench: Domain-specific LLM evaluation for fashion industry")


# Define available evaluations
EVALUATIONS = {
    "trend_detection": {
        "name": "Trend Detection",
        "description": "Identify fashion trends from social media and runway data",
        "function": evaluate_trend_detection
    },
    "product_extraction": {
        "name": "Product Extraction",
        "description": "Extract structured product info from unstructured content",
        "function": evaluate_product_extraction
    },
    "style_classification": {
        "name": "Style Classification",
        "description": "Classify fashion styles and aesthetics",
        "function": evaluate_style_classification
    },
    "fashion_writing": {
        "name": "Fashion Writing",
        "description": "Generate engaging fashion content and captions",
        "function": evaluate_fashion_writing
    },
    "hashtag_understanding": {
        "name": "Hashtag Understanding",
        "description": "Understand fashion-specific hashtags and their context",
        "function": evaluate_hashtag_understanding
    },
    "affiliate_detection": {
        "name": "Affiliate Detection",
        "description": "Detect affiliate marketing and sponsored content",
        "function": evaluate_affiliate_detection
    }
}


def print_header():
    """Print FashionBench header."""
    header = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                     FASHIONBENCH                          ║
    ║          Fashion Industry LLM Evaluation Suite            ║
    ║                                                           ║
    ║        The world's first domain-specific benchmark        ║
    ║           for fashion & influencer marketing              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(header, style="bold magenta")


def print_results_table(all_results: list):
    """
    Print formatted results table using Rich.

    Args:
        all_results: List of evaluation result dictionaries
    """
    table = Table(title="FashionBench Results", box=box.ROUNDED)

    table.add_column("Evaluation", style="cyan", no_wrap=True)
    table.add_column("Examples", justify="center", style="white")
    table.add_column("Passed", justify="center", style="green")
    table.add_column("Avg Score", justify="center", style="yellow")
    table.add_column("Status", justify="center")

    total_examples = 0
    total_passed = 0
    total_score = 0.0

    for result in all_results:
        eval_name = result["eval_name"]
        examples = result["total_examples"]
        passed = result["passed"]
        avg_score = result["avg_score"]

        total_examples += examples
        total_passed += passed
        total_score += avg_score

        # Status emoji
        pass_rate = passed / examples if examples > 0 else 0
        if pass_rate >= 0.8:
            status = "✓ Excellent"
            status_style = "bold green"
        elif pass_rate >= 0.6:
            status = "○ Good"
            status_style = "yellow"
        else:
            status = "✗ Needs Work"
            status_style = "red"

        table.add_row(
            eval_name,
            str(examples),
            f"{passed}/{examples}",
            f"{avg_score:.3f}",
            status,
            style=status_style if pass_rate < 0.6 else None
        )

    # Add summary row
    avg_overall = total_score / len(all_results) if all_results else 0
    table.add_section()
    table.add_row(
        "OVERALL",
        str(total_examples),
        f"{total_passed}/{total_examples}",
        f"{avg_overall:.3f}",
        "Summary",
        style="bold white"
    )

    console.print("\n")
    console.print(table)
    console.print("\n")


@app.command()
def run(
    model: str = typer.Option("simulated", "--model", "-m", help="Model name to evaluate (e.g., claude-3-sonnet, gpt-4)"),
    eval_name: Optional[str] = typer.Option(None, "--eval", "-e", help="Specific evaluation to run (omit to run all)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
    list_evals: bool = typer.Option(False, "--list", "-l", help="List all available evaluations")
):
    """
    Run FashionBench evaluations on a specified model.

    Examples:
        python run_fashionbench.py --model claude-3-sonnet
        python run_fashionbench.py --model gpt-4 --eval trend_detection
        python run_fashionbench.py --list
    """

    # List evaluations if requested
    if list_evals:
        console.print("\n[bold cyan]Available Evaluations:[/bold cyan]\n")
        for key, info in EVALUATIONS.items():
            console.print(f"  • [green]{key}[/green]: {info['description']}")
        console.print("\n")
        return

    print_header()

    console.print(f"[bold]Model:[/bold] {model}")
    console.print(f"[bold]Mode:[/bold] {'Single Eval' if eval_name else 'Full Suite'}\n")

    # Determine which evaluations to run
    if eval_name:
        if eval_name not in EVALUATIONS:
            console.print(f"[red]Error: Unknown evaluation '{eval_name}'[/red]")
            console.print(f"[yellow]Use --list to see available evaluations[/yellow]")
            sys.exit(1)
        evals_to_run = {eval_name: EVALUATIONS[eval_name]}
    else:
        evals_to_run = EVALUATIONS

    # Run evaluations
    all_results = []

    with console.status("[bold green]Running evaluations...", spinner="dots") as status:
        for key, eval_info in evals_to_run.items():
            status.update(f"[bold green]Running {eval_info['name']}...")

            try:
                # Run evaluation (suppress output if not verbose)
                if not verbose:
                    # Redirect stdout temporarily
                    import io
                    old_stdout = sys.stdout
                    sys.stdout = io.StringIO()

                result = eval_info["function"](model_name=model)

                if not verbose:
                    sys.stdout = old_stdout

                all_results.append(result)

                console.print(f"[green]✓[/green] {eval_info['name']} completed")

            except Exception as e:
                if not verbose:
                    sys.stdout = old_stdout
                console.print(f"[red]✗[/red] {eval_info['name']} failed: {str(e)}")
                continue

    # Print results
    if all_results:
        print_results_table(all_results)

        # Print summary
        avg_score = sum(r["avg_score"] for r in all_results) / len(all_results)

        if avg_score >= 0.8:
            grade = "A"
            color = "green"
            message = "Excellent performance on fashion domain tasks!"
        elif avg_score >= 0.7:
            grade = "B"
            color = "yellow"
            message = "Good performance with room for improvement."
        elif avg_score >= 0.6:
            grade = "C"
            color = "yellow"
            message = "Moderate performance. Consider fine-tuning."
        else:
            grade = "D"
            color = "red"
            message = "Needs significant improvement for fashion tasks."

        summary = Panel(
            f"[bold]Overall Grade: {grade}[/bold]\n"
            f"Average Score: {avg_score:.3f}\n\n"
            f"{message}",
            title="Summary",
            border_style=color
        )
        console.print(summary)

    else:
        console.print("[red]No evaluations completed successfully.[/red]")

    # Footer
    console.print("\n[dim]Created by Ortal | ortal@onsight-analytics.com[/dim]")


@app.command()
def info():
    """Show information about FashionBench."""
    print_header()

    info_text = """
    [bold cyan]About FashionBench[/bold cyan]

    FashionBench is the world's first domain-specific benchmark suite for evaluating
    LLM performance in the fashion industry. It tests critical capabilities needed
    for fashion content creation, trend analysis, and influencer marketing.

    [bold cyan]Evaluation Categories:[/bold cyan]

    1. Trend Detection - Identify emerging fashion trends
    2. Product Extraction - Extract structured product data
    3. Style Classification - Classify fashion aesthetics
    4. Fashion Writing - Generate engaging content
    5. Hashtag Understanding - Decode fashion social media
    6. Affiliate Detection - Identify monetization strategies

    [bold cyan]Creator:[/bold cyan]
    Ortal - Vibe Coder & Vibe Solver
    Email: ortal@onsight-analytics.com

    [bold cyan]Usage:[/bold cyan]
    python run_fashionbench.py --model <model_name>
    python run_fashionbench.py --list
    python run_fashionbench.py --help
    """

    console.print(Panel(info_text, title="FashionBench Info", border_style="magenta"))


if __name__ == "__main__":
    app()
