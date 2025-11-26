"""
Style Classification Evaluation Script

This script evaluates an LLM's ability to classify fashion styles and aesthetics
based on outfit descriptions, identifying categories like bohemian, streetwear,
corporate, quiet luxury, and more.
"""

import jsonlines
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from scoring.metrics import exact_match, fashion_similarity


def load_dataset(dataset_path: str) -> list:
    """
    Load the style classification dataset from JSONL file.

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


def classify_style(description: str) -> str:
    """
    Simple style classification logic for demonstration.
    In production, this would use the actual LLM.

    Args:
        description: Outfit description text

    Returns:
        Predicted style category
    """
    description_lower = description.lower()

    # Keyword-based classification for demo
    if any(word in description_lower for word in ["blazer", "trousers", "professional", "tote", "corporate"]):
        return "Corporate/Professional"
    elif any(word in description_lower for word in ["leather jacket", "distressed", "combat boots", "grunge", "band t-shirt"]):
        return "Grunge/Rock"
    elif any(word in description_lower for word in ["floral", "maxi dress", "basket bag", "bohemian", "woven"]):
        return "Bohemian/Boho"
    elif any(word in description_lower for word in ["hoodie", "joggers", "sneakers", "athleisure", "sporty"]):
        return "Athleisure/Sporty"
    elif any(word in description_lower for word in ["cashmere", "quiet luxury", "minimalist", "tailored wool"]):
        return "Quiet Luxury/Minimalist"
    elif any(word in description_lower for word in ["streetwear", "baggy jeans", "nike", "puffer", "urban"]):
        return "Streetwear/Urban"
    elif any(word in description_lower for word in ["coquette", "pastel", "ribbon", "pearl", "feminine"]):
        return "Coquette/Feminine"
    elif any(word in description_lower for word in ["hypebeast", "cargo pants", "bucket hat", "chains"]):
        return "Hypebeast/Streetwear"
    elif any(word in description_lower for word in ["linen", "espadrilles", "coastal", "resort", "straw hat"]):
        return "Coastal/Resort"
    elif any(word in description_lower for word in ["tweed", "classic", "timeless", "kitten heels"]):
        return "Classic/Timeless"
    else:
        return "Contemporary/Mixed"


def simulate_model_response(example: dict, model_name: str) -> str:
    """
    Simulate a model response for style classification.
    In production, this would call actual LLM APIs.

    Args:
        example: Dataset example containing description
        model_name: Name of the model to simulate

    Returns:
        Predicted style category
    """
    description = example.get("description", "")
    return classify_style(description)


def evaluate_style_classification(model_name: str = "simulated", dataset_path: str = None) -> dict:
    """
    Evaluate model performance on style classification tasks.

    Args:
        model_name: Name of the model to evaluate
        dataset_path: Path to dataset file (optional)

    Returns:
        Dictionary containing evaluation results and metrics
    """
    if dataset_path is None:
        dataset_path = Path(__file__).parent.parent / "datasets" / "style_classification.jsonl"

    examples = load_dataset(str(dataset_path))
    results = []
    total_score = 0

    print(f"\n{'='*60}")
    print(f"Evaluating Style Classification - Model: {model_name}")
    print(f"{'='*60}\n")

    for example in examples:
        # Get model response
        model_output = simulate_model_response(example, model_name)
        expected = example["expected"]

        # Calculate score
        # Use exact match with fallback to similarity
        exact_score = exact_match(model_output, expected)
        if exact_score < 1.0:
            similarity_score = fashion_similarity(model_output, expected)
            score = max(exact_score, similarity_score)
        else:
            score = exact_score

        total_score += score

        results.append({
            "id": example["id"],
            "description": example["description"],
            "expected": expected,
            "model_output": model_output,
            "score": score
        })

        # Print individual result
        status = "✓" if score >= 0.7 else "✗"
        print(f"{status} Example {example['id']}: {score:.2f}")
        print(f"  Description: {example['description'][:50]}...")
        print(f"  Expected: {expected}")
        print(f"  Predicted: {model_output}\n")

    # Calculate overall metrics
    avg_score = total_score / len(examples) if examples else 0
    passed = sum(1 for r in results if r["score"] >= 0.7)

    print(f"{'='*60}")
    print(f"Results: {passed}/{len(examples)} passed (threshold: 0.7)")
    print(f"Average Score: {avg_score:.3f}")
    print(f"{'='*60}\n")

    return {
        "eval_name": "Style Classification",
        "model": model_name,
        "total_examples": len(examples),
        "passed": passed,
        "avg_score": avg_score,
        "results": results
    }


if __name__ == "__main__":
    # Run evaluation when script is executed directly
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate style classification capabilities")
    parser.add_argument("--model", default="simulated", help="Model name to evaluate")
    parser.add_argument("--dataset", default=None, help="Path to dataset file")

    args = parser.parse_args()
    evaluate_style_classification(args.model, args.dataset)
