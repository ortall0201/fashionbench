"""
Affiliate Detection Evaluation Script

This script evaluates an LLM's ability to detect affiliate marketing, sponsored content,
discount codes, and monetization strategies in fashion social media posts.
"""

import jsonlines
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from scoring.metrics import exact_match


def load_dataset(dataset_path: str) -> list:
    """
    Load the affiliate detection dataset from JSONL file.

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


def detect_affiliate_content(text: str) -> dict:
    """
    Simple affiliate detection logic for demonstration.
    In production, this would use the actual LLM.

    Args:
        text: Post text to analyze

    Returns:
        Dictionary with affiliate detection results
    """
    result = {"has_affiliate": False}
    text_lower = text.lower()

    # Detect affiliate platforms
    if "ltk" in text_lower or "liketoknow" in text_lower:
        result["has_affiliate"] = True
        result["platform"] = "LTK"
        if "shop.ltk" in text_lower:
            result["platform"] = "ShopLTK"

    # Detect Amazon affiliate
    if "amazon" in text_lower and ("storefront" in text_lower or "finds" in text_lower):
        result["has_affiliate"] = True
        result["platform"] = "Amazon"
        result["type"] = "affiliate_storefront"

    # Detect discount codes
    import re
    code_pattern = r'code\s+(\w+)'
    codes = re.findall(code_pattern, text, re.IGNORECASE)
    if codes:
        result["has_affiliate"] = True
        result["type"] = "discount_code" if not result.get("type") else result["type"]
        result["code"] = codes[0]

        # Try to detect discount percentage
        discount_pattern = r'(\d+)%'
        discounts = re.findall(discount_pattern, text)
        if discounts:
            result["discount"] = f"{discounts[0]}%"

    # Detect sponsored content
    sponsored_keywords = ["#ad", "#gifted", "#sponsored", "paid partnership", "partnering"]
    found_disclosures = [kw for kw in sponsored_keywords if kw in text_lower]
    if found_disclosures:
        result["has_affiliate"] = True
        result["type"] = "sponsored"
        result["disclosures"] = found_disclosures

    # Detect brand partnerships
    if "partnering" in text_lower or "partnership" in text_lower:
        result["type"] = "brand_partnership" if result.get("has_affiliate") else result.get("type")

    # Check for organic content indicators
    if not result["has_affiliate"]:
        if "thrifted" in text_lower or "no links" in text_lower or "just sharing" in text_lower:
            result["type"] = "organic"

    # Detect link mentions
    if "link" in text_lower or "swipe up" in text_lower or "tap to shop" in text_lower:
        result["has_affiliate"] = True
        if "indicators" not in result:
            result["indicators"] = []
        if "link" in text_lower:
            result["indicators"].append("link in bio")

    return result


def simulate_model_response(example: dict, model_name: str) -> dict:
    """
    Simulate a model response for affiliate detection.
    In production, this would call actual LLM APIs.

    Args:
        example: Dataset example containing text
        model_name: Name of the model to simulate

    Returns:
        Dictionary with affiliate detection results
    """
    text = example.get("text", "")
    return detect_affiliate_content(text)


def calculate_affiliate_score(predicted: dict, expected: dict) -> float:
    """
    Calculate affiliate detection score.

    Args:
        predicted: Predicted affiliate information
        expected: Expected affiliate information

    Returns:
        Score between 0 and 1
    """
    if not expected:
        return 0.0

    score = 0.0
    components = 0

    # Check has_affiliate (most important)
    if "has_affiliate" in expected:
        components += 2  # Weight this more heavily
        if predicted.get("has_affiliate") == expected["has_affiliate"]:
            score += 2.0

    # Check platform
    if "platform" in expected:
        components += 1
        if predicted.get("platform", "").lower() == expected["platform"].lower():
            score += 1.0

    # Check type
    if "type" in expected:
        components += 1
        if predicted.get("type", "").lower() == expected["type"].lower():
            score += 1.0
        elif expected["type"] in str(predicted.get("type", "")):
            score += 0.5

    # Check discount code
    if "code" in expected:
        components += 1
        if predicted.get("code", "").upper() == expected["code"].upper():
            score += 1.0

    # Check discount percentage
    if "discount" in expected:
        components += 0.5
        if predicted.get("discount") == expected["discount"]:
            score += 0.5

    # Check disclosures
    if "disclosures" in expected:
        components += 1
        expected_disclosures = set(d.lower() for d in expected["disclosures"])
        predicted_disclosures = set(d.lower() for d in predicted.get("disclosures", []))
        overlap = len(expected_disclosures & predicted_disclosures)
        if overlap > 0:
            score += overlap / len(expected_disclosures)

    return score / components if components > 0 else 0.0


def evaluate_affiliate_detection(model_name: str = "simulated", dataset_path: str = None) -> dict:
    """
    Evaluate model performance on affiliate detection tasks.

    Args:
        model_name: Name of the model to evaluate
        dataset_path: Path to dataset file (optional)

    Returns:
        Dictionary containing evaluation results and metrics
    """
    if dataset_path is None:
        dataset_path = Path(__file__).parent.parent / "datasets" / "affiliate_detection.jsonl"

    examples = load_dataset(str(dataset_path))
    results = []
    total_score = 0

    print(f"\n{'='*60}")
    print(f"Evaluating Affiliate Detection - Model: {model_name}")
    print(f"{'='*60}\n")

    for example in examples:
        # Get model response
        model_output = simulate_model_response(example, model_name)
        expected = example["expected"]

        # Calculate score
        score = calculate_affiliate_score(model_output, expected)
        total_score += score

        results.append({
            "id": example["id"],
            "text": example["text"],
            "expected": expected,
            "model_output": model_output,
            "score": score
        })

        # Print individual result
        status = "✓" if score >= 0.7 else "✗"
        print(f"{status} Example {example['id']}: {score:.2f}")
        print(f"  Text: {example['text'][:60]}...")
        print(f"  Expected: {json.dumps(expected, indent=2)}")
        print(f"  Detected: {json.dumps(model_output, indent=2)}\n")

    # Calculate overall metrics
    avg_score = total_score / len(examples) if examples else 0
    passed = sum(1 for r in results if r["score"] >= 0.7)

    print(f"{'='*60}")
    print(f"Results: {passed}/{len(examples)} passed (threshold: 0.7)")
    print(f"Average Score: {avg_score:.3f}")
    print(f"{'='*60}\n")

    return {
        "eval_name": "Affiliate Detection",
        "model": model_name,
        "total_examples": len(examples),
        "passed": passed,
        "avg_score": avg_score,
        "results": results
    }


if __name__ == "__main__":
    # Run evaluation when script is executed directly
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate affiliate detection capabilities")
    parser.add_argument("--model", default="simulated", help="Model name to evaluate")
    parser.add_argument("--dataset", default=None, help="Path to dataset file")

    args = parser.parse_args()
    evaluate_affiliate_detection(args.model, args.dataset)
