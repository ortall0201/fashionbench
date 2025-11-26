"""
Fashion Writing Evaluation Script

This script evaluates an LLM's ability to create engaging fashion content,
including caption rewriting, style descriptions, and brand voice adaptation.
"""

import jsonlines
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from scoring.metrics import partial_match, fashion_similarity


def load_dataset(dataset_path: str) -> list:
    """
    Load the caption rewriting dataset from JSONL file.

    Args:
        dataset_path: Path to the JSONL dataset file

    Returns:
        List of dataset examples
    """
    examples = []
    with jsonlines.open(dataset_path) as reader:
        for obj in reader:
            examples.append(obj)
    return examples


def rewrite_caption(original: str, context: str, style: str) -> str:
    """
    Simple caption rewriting logic for demonstration.
    In production, this would use the actual LLM.

    Args:
        original: Original simple caption
        context: Context about the outfit/item
        style: Desired writing style

    Returns:
        Rewritten engaging caption
    """
    # Simple template-based rewriting for demo
    context_lower = context.lower()

    if "blazer" in context_lower and "jeans" in context_lower:
        return "Elevated casual perfection: tailored blazer meets classic denim. Sophisticated yet comfortable."
    elif "floral" in context_lower and "midi" in context_lower:
        return "Spring blooms in this dreamy floral midi. Effortless elegance with garden party charm."
    elif "sneakers" in context_lower and "white" in context_lower:
        return "Statement sneakers that steal the show. Clean, bold, endlessly wearable."
    elif "little black dress" in context_lower or "lbd" in context_lower:
        return "That LBD energy: timeless, confident, unforgettable. When the dress speaks volumes."
    elif "sweater" in context_lower and "leggings" in context_lower:
        return "Cozy season done right: wrapped in comfort without sacrificing style."
    elif "pencil skirt" in context_lower and "blouse" in context_lower:
        return "Boardroom ready: polished power dressing meets feminine sophistication."
    elif "vintage" in context_lower or "thrifted" in context_lower:
        return "Sustainable style wins: this vintage treasure proves pre-loved is best. Thrifted, not bought."
    elif "linen" in context_lower and "summer" in context_lower:
        return "Sun-soaked sophistication: breezy linens for endless summer days. Vacation mode on."
    elif "coat" in context_lower and "bold" in context_lower:
        return "That compliment magnet: when your coat steals the spotlight. Bold moves, big impact."
    elif "loungewear" in context_lower:
        return "Elevated lounging: staying in never looked this chic. Cozy, coordinated, completely stylish."
    else:
        return f"Transformed from '{original}' into elevated fashion content with {style} vibes."


def simulate_model_response(example: dict, model_name: str) -> str:
    """
    Simulate a model response for caption rewriting.
    In production, this would call actual LLM APIs.

    Args:
        example: Dataset example containing original caption
        model_name: Name of the model to simulate

    Returns:
        Rewritten caption
    """
    original = example.get("original", "")
    context = example.get("context", "")
    style = example.get("style", "professional")

    return rewrite_caption(original, context, style)


def evaluate_writing_quality(generated: str, expected: str) -> float:
    """
    Evaluate writing quality by checking key elements.

    Args:
        generated: Generated caption text
        expected: Expected caption text

    Returns:
        Quality score between 0 and 1
    """
    score = 0.0
    weights = []

    # Check length (good captions should be substantial)
    if len(generated) > 50:
        score += 0.2
        weights.append(1)
    else:
        weights.append(1)

    # Check for descriptive words (elevated vocabulary)
    descriptive_words = ["elevated", "chic", "sophisticated", "effortless", "timeless", "bold", "dreamy", "cozy"]
    if any(word in generated.lower() for word in descriptive_words):
        score += 0.3
        weights.append(1)
    else:
        weights.append(1)

    # Check structure (should have multiple sentences or clauses)
    if generated.count('.') >= 1 or generated.count(':') >= 1:
        score += 0.2
        weights.append(1)
    else:
        weights.append(1)

    # Semantic similarity to expected
    similarity = fashion_similarity(generated, expected)
    score += similarity * 0.3
    weights.append(1)

    return score


def evaluate_fashion_writing(model_name: str = "simulated", dataset_path: str = None) -> dict:
    """
    Evaluate model performance on fashion writing tasks.

    Args:
        model_name: Name of the model to evaluate
        dataset_path: Path to dataset file (optional)

    Returns:
        Dictionary containing evaluation results and metrics
    """
    if dataset_path is None:
        dataset_path = Path(__file__).parent.parent / "datasets" / "caption_rewriting.jsonl"

    examples = load_dataset(str(dataset_path))
    results = []
    total_score = 0

    print(f"\n{'='*60}")
    print(f"Evaluating Fashion Writing - Model: {model_name}")
    print(f"{'='*60}\n")

    for example in examples:
        # Get model response
        model_output = simulate_model_response(example, model_name)
        expected = example["expected"]

        # Calculate score
        score = evaluate_writing_quality(model_output, expected)
        total_score += score

        results.append({
            "id": example["id"],
            "original": example["original"],
            "context": example["context"],
            "expected": expected,
            "model_output": model_output,
            "score": score
        })

        # Print individual result
        status = "✓" if score >= 0.6 else "✗"
        print(f"{status} Example {example['id']}: {score:.2f}")
        print(f"  Original: '{example['original']}'")
        print(f"  Generated: {model_output}")
        print(f"  Expected: {expected}\n")

    # Calculate overall metrics
    avg_score = total_score / len(examples) if examples else 0
    passed = sum(1 for r in results if r["score"] >= 0.6)

    print(f"{'='*60}")
    print(f"Results: {passed}/{len(examples)} passed (threshold: 0.6)")
    print(f"Average Score: {avg_score:.3f}")
    print(f"{'='*60}\n")

    return {
        "eval_name": "Fashion Writing",
        "model": model_name,
        "total_examples": len(examples),
        "passed": passed,
        "avg_score": avg_score,
        "results": results
    }


if __name__ == "__main__":
    # Run evaluation when script is executed directly
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate fashion writing capabilities")
    parser.add_argument("--model", default="simulated", help="Model name to evaluate")
    parser.add_argument("--dataset", default=None, help="Path to dataset file")

    args = parser.parse_args()
    evaluate_fashion_writing(args.model, args.dataset)
