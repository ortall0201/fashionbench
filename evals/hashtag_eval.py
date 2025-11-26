"""
Hashtag Understanding Evaluation Script

This script evaluates an LLM's ability to understand fashion-specific hashtags,
their meanings, contexts, and purposes in social media content.
"""

import jsonlines
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from scoring.metrics import exact_match, partial_match


def load_dataset(dataset_path: str) -> list:
    """
    Load the hashtag understanding dataset from JSONL file.

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


def understand_hashtag(hashtag: str, context: str) -> dict:
    """
    Simple hashtag understanding logic for demonstration.
    In production, this would use the actual LLM.

    Args:
        hashtag: The hashtag to understand
        context: Context in which hashtag is used

    Returns:
        Dictionary with hashtag meaning, category, and purpose
    """
    hashtag_lower = hashtag.lower()

    # Hashtag knowledge base for demo
    hashtag_db = {
        "#ootd": {
            "meaning": "Outfit Of The Day",
            "category": "outfit_sharing",
            "purpose": "showcase daily outfit choice"
        },
        "#grwm": {
            "meaning": "Get Ready With Me",
            "category": "lifestyle_content",
            "purpose": "document preparation routine"
        },
        "#tryonhaul": {
            "meaning": "Try On Haul",
            "category": "shopping_content",
            "purpose": "show purchased items being worn"
        },
        "#iykyk": {
            "meaning": "If You Know You Know",
            "category": "insider_reference",
            "purpose": "subtle flex or insider knowledge"
        },
        "#dupealert": {
            "meaning": "Dupe Alert",
            "category": "budget_fashion",
            "purpose": "share affordable alternative"
        },
        "#ootw": {
            "meaning": "Outfit Of The Week",
            "category": "outfit_sharing",
            "purpose": "showcase weekly outfit choices"
        },
        "#ltk": {
            "meaning": "LikeToKnowIt",
            "category": "affiliate_marketing",
            "purpose": "monetize through affiliate links"
        },
        "#shein": {
            "meaning": "SHEIN brand",
            "category": "brand_tag",
            "purpose": "tag fast fashion retailer"
        },
        "#thriftflip": {
            "meaning": "Thrift Flip",
            "category": "sustainable_fashion",
            "purpose": "show thrifted item upcycle"
        },
        "#wiwtd": {
            "meaning": "What I Wore Today",
            "category": "outfit_sharing",
            "purpose": "share outfit for specific day"
        }
    }

    return hashtag_db.get(hashtag_lower, {
        "meaning": "Unknown hashtag",
        "category": "general",
        "purpose": "social media engagement"
    })


def simulate_model_response(example: dict, model_name: str) -> dict:
    """
    Simulate a model response for hashtag understanding.
    In production, this would call actual LLM APIs.

    Args:
        example: Dataset example containing hashtag and context
        model_name: Name of the model to simulate

    Returns:
        Dictionary with hashtag interpretation
    """
    hashtag = example.get("hashtag", "")
    context = example.get("context", "")

    return understand_hashtag(hashtag, context)


def calculate_hashtag_score(predicted: dict, expected: dict) -> float:
    """
    Calculate hashtag understanding score.

    Args:
        predicted: Predicted hashtag information
        expected: Expected hashtag information

    Returns:
        Score between 0 and 1
    """
    if not expected or not predicted:
        return 0.0

    score = 0.0
    total_components = 3  # meaning, category, purpose

    # Check meaning
    if "meaning" in expected and "meaning" in predicted:
        if expected["meaning"].lower() == predicted["meaning"].lower():
            score += 1.0
        elif expected["meaning"].lower() in predicted["meaning"].lower() or predicted["meaning"].lower() in expected["meaning"].lower():
            score += 0.7

    # Check category
    if "category" in expected and "category" in predicted:
        if expected["category"].lower() == predicted["category"].lower():
            score += 1.0
        elif expected["category"].lower() in predicted["category"].lower() or predicted["category"].lower() in expected["category"].lower():
            score += 0.5

    # Check purpose
    if "purpose" in expected and "purpose" in predicted:
        expected_purpose = expected["purpose"].lower()
        predicted_purpose = predicted["purpose"].lower()

        if expected_purpose == predicted_purpose:
            score += 1.0
        elif expected_purpose in predicted_purpose or predicted_purpose in expected_purpose:
            score += 0.7
        else:
            # Check for key overlapping words
            expected_words = set(expected_purpose.split())
            predicted_words = set(predicted_purpose.split())
            overlap = len(expected_words & predicted_words)
            if overlap > 0:
                score += 0.4

    return score / total_components


def evaluate_hashtag_understanding(model_name: str = "simulated", dataset_path: str = None) -> dict:
    """
    Evaluate model performance on hashtag understanding tasks.

    Args:
        model_name: Name of the model to evaluate
        dataset_path: Path to dataset file (optional)

    Returns:
        Dictionary containing evaluation results and metrics
    """
    if dataset_path is None:
        dataset_path = Path(__file__).parent.parent / "datasets" / "hashtag_understanding.jsonl"

    examples = load_dataset(str(dataset_path))
    results = []
    total_score = 0

    print(f"\n{'='*60}")
    print(f"Evaluating Hashtag Understanding - Model: {model_name}")
    print(f"{'='*60}\n")

    for example in examples:
        # Get model response
        model_output = simulate_model_response(example, model_name)
        expected = example["expected"]

        # Calculate score
        score = calculate_hashtag_score(model_output, expected)
        total_score += score

        results.append({
            "id": example["id"],
            "hashtag": example["hashtag"],
            "context": example["context"],
            "expected": expected,
            "model_output": model_output,
            "score": score
        })

        # Print individual result
        status = "✓" if score >= 0.7 else "✗"
        print(f"{status} Example {example['id']}: {score:.2f}")
        print(f"  Hashtag: {example['hashtag']}")
        print(f"  Expected: {json.dumps(expected, indent=2)}")
        print(f"  Predicted: {json.dumps(model_output, indent=2)}\n")

    # Calculate overall metrics
    avg_score = total_score / len(examples) if examples else 0
    passed = sum(1 for r in results if r["score"] >= 0.7)

    print(f"{'='*60}")
    print(f"Results: {passed}/{len(examples)} passed (threshold: 0.7)")
    print(f"Average Score: {avg_score:.3f}")
    print(f"{'='*60}\n")

    return {
        "eval_name": "Hashtag Understanding",
        "model": model_name,
        "total_examples": len(examples),
        "passed": passed,
        "avg_score": avg_score,
        "results": results
    }


if __name__ == "__main__":
    # Run evaluation when script is executed directly
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate hashtag understanding capabilities")
    parser.add_argument("--model", default="simulated", help="Model name to evaluate")
    parser.add_argument("--dataset", default=None, help="Path to dataset file")

    args = parser.parse_args()
    evaluate_hashtag_understanding(args.model, args.dataset)
