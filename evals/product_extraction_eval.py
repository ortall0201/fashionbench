"""
Product Extraction Evaluation Script

This script evaluates an LLM's ability to extract structured product information
from unstructured fashion content, including brands, prices, links, and discount codes.
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
    Load the product extraction dataset from JSONL file.

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


def extract_key_info(text: str) -> dict:
    """
    Simple extraction logic for demonstration.
    In production, this would use the actual LLM.

    Args:
        text: Input text containing product information

    Returns:
        Dictionary of extracted product information
    """
    result = {}

    # Brand detection (simple keyword matching for demo)
    brands = ["Zara", "Reformation", "Nike", "Levi's", "H&M", "Jacquemus", "Chanel", "Mango", "Bottega Veneta", "Skims"]
    for brand in brands:
        if brand in text:
            result["brand"] = brand
            break

    # Price detection
    import re
    price_pattern = r'[\$€£]\d+(?:\.\d{2})?'
    prices = re.findall(price_pattern, text)
    if prices:
        result["price"] = prices[0]

    # Discount code detection
    code_pattern = r'code\s+(\w+)'
    codes = re.findall(code_pattern, text, re.IGNORECASE)
    if codes:
        result["discount_code"] = codes[0]

    # Link detection
    if "link" in text.lower() or "http" in text:
        result["link_mentioned"] = True
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        if urls:
            result["link"] = urls[0]

    # Affiliate platform detection
    if "LTK" in text or "ltk" in text.lower():
        result["affiliate_platform"] = "LTK" if "LTK" in text else "ShopLTK"

    return result


def simulate_model_response(example: dict, model_name: str) -> dict:
    """
    Simulate a model response for product extraction.
    In production, this would call actual LLM APIs.

    Args:
        example: Dataset example containing text
        model_name: Name of the model to simulate

    Returns:
        Extracted product information as dictionary
    """
    text = example.get("text", "")
    return extract_key_info(text)


def calculate_extraction_score(predicted: dict, expected: dict) -> float:
    """
    Calculate extraction score by comparing predicted and expected fields.

    Args:
        predicted: Predicted product information
        expected: Expected product information

    Returns:
        Score between 0 and 1
    """
    if not expected:
        return 0.0

    # Handle nested items list if present
    if "items" in expected:
        # Complex multi-item extraction
        return 0.5  # Simplified for demo

    # Calculate field-level accuracy
    total_fields = len(expected)
    correct_fields = 0

    for key, expected_value in expected.items():
        if key in predicted:
            if isinstance(expected_value, bool):
                if predicted[key] == expected_value:
                    correct_fields += 1
            elif isinstance(expected_value, str):
                if predicted[key].lower() == expected_value.lower():
                    correct_fields += 1
                elif expected_value.lower() in predicted[key].lower() or predicted[key].lower() in expected_value.lower():
                    correct_fields += 0.7  # Partial match
            else:
                if predicted[key] == expected_value:
                    correct_fields += 1

    return correct_fields / total_fields if total_fields > 0 else 0.0


def evaluate_product_extraction(model_name: str = "simulated", dataset_path: str = None) -> dict:
    """
    Evaluate model performance on product extraction tasks.

    Args:
        model_name: Name of the model to evaluate
        dataset_path: Path to dataset file (optional)

    Returns:
        Dictionary containing evaluation results and metrics
    """
    if dataset_path is None:
        dataset_path = Path(__file__).parent.parent / "datasets" / "product_extraction.jsonl"

    examples = load_dataset(str(dataset_path))
    results = []
    total_score = 0

    print(f"\n{'='*60}")
    print(f"Evaluating Product Extraction - Model: {model_name}")
    print(f"{'='*60}\n")

    for example in examples:
        # Get model response
        model_output = simulate_model_response(example, model_name)
        expected = example["expected"]

        # Calculate score
        score = calculate_extraction_score(model_output, expected)
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
        print(f"  Extracted: {json.dumps(model_output, indent=2)}\n")

    # Calculate overall metrics
    avg_score = total_score / len(examples) if examples else 0
    passed = sum(1 for r in results if r["score"] >= 0.7)

    print(f"{'='*60}")
    print(f"Results: {passed}/{len(examples)} passed (threshold: 0.7)")
    print(f"Average Score: {avg_score:.3f}")
    print(f"{'='*60}\n")

    return {
        "eval_name": "Product Extraction",
        "model": model_name,
        "total_examples": len(examples),
        "passed": passed,
        "avg_score": avg_score,
        "results": results
    }


if __name__ == "__main__":
    # Run evaluation when script is executed directly
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate product extraction capabilities")
    parser.add_argument("--model", default="simulated", help="Model name to evaluate")
    parser.add_argument("--dataset", default=None, help="Path to dataset file")

    args = parser.parse_args()
    evaluate_product_extraction(args.model, args.dataset)
