"""
Scoring Metrics for FashionBench

This module provides various scoring functions for evaluating LLM performance
on fashion-specific tasks. Includes exact match, partial match, and custom
fashion similarity metrics.
"""

from typing import Union, List
import re


def exact_match(predicted: str, expected: str) -> float:
    """
    Calculate exact match score between predicted and expected strings.

    Args:
        predicted: Model's predicted output
        expected: Expected correct output

    Returns:
        1.0 if exact match (case-insensitive), 0.0 otherwise
    """
    if not predicted or not expected:
        return 0.0

    predicted_clean = predicted.strip().lower()
    expected_clean = expected.strip().lower()

    return 1.0 if predicted_clean == expected_clean else 0.0


def partial_match(predicted: str, expected: str, threshold: float = 0.5) -> float:
    """
    Calculate partial match score based on word overlap.

    Args:
        predicted: Model's predicted output
        expected: Expected correct output
        threshold: Minimum overlap ratio to consider a match

    Returns:
        Score between 0.0 and 1.0 based on word overlap
    """
    if not predicted or not expected:
        return 0.0

    # Tokenize into words
    predicted_words = set(re.findall(r'\w+', predicted.lower()))
    expected_words = set(re.findall(r'\w+', expected.lower()))

    if not expected_words:
        return 0.0

    # Calculate overlap
    intersection = predicted_words & expected_words
    union = predicted_words | expected_words

    # Jaccard similarity
    jaccard = len(intersection) / len(union) if union else 0.0

    # Also calculate recall (what proportion of expected words were found)
    recall = len(intersection) / len(expected_words)

    # Return average of Jaccard and recall
    score = (jaccard + recall) / 2

    return score


def fashion_similarity(predicted: str, expected: str) -> float:
    """
    Custom fashion-specific similarity metric.
    Accounts for fashion terminology, synonyms, and domain-specific concepts.

    Args:
        predicted: Model's predicted output
        expected: Expected correct output

    Returns:
        Score between 0.0 and 1.0 based on fashion-aware similarity
    """
    if not predicted or not expected:
        return 0.0

    predicted_lower = predicted.lower()
    expected_lower = expected.lower()

    # Define fashion synonym groups
    fashion_synonyms = {
        "luxury": ["high-end", "premium", "upscale", "designer"],
        "casual": ["relaxed", "laid-back", "comfortable", "easy"],
        "elegant": ["sophisticated", "refined", "polished", "chic"],
        "trendy": ["fashionable", "stylish", "on-trend", "contemporary"],
        "vintage": ["retro", "classic", "throwback", "timeless"],
        "minimalist": ["simple", "clean", "understated", "minimal"],
        "bohemian": ["boho", "hippie", "free-spirited", "eclectic"],
        "streetwear": ["urban", "street-style", "casual-cool"],
        "athleisure": ["sporty", "athletic", "activewear"],
        "sustainable": ["eco-friendly", "ethical", "conscious", "green"],
    }

    score = 0.0

    # Check for exact match first
    if predicted_lower == expected_lower:
        return 1.0

    # Check if predicted contains expected or vice versa
    if expected_lower in predicted_lower or predicted_lower in expected_lower:
        return 0.9

    # Tokenize
    predicted_words = set(re.findall(r'\w+', predicted_lower))
    expected_words = set(re.findall(r'\w+', expected_lower))

    # Calculate base overlap
    direct_overlap = predicted_words & expected_words
    base_score = len(direct_overlap) / len(expected_words) if expected_words else 0.0

    # Check for synonym matches
    synonym_matches = 0
    expected_word_count = len(expected_words)

    for exp_word in expected_words:
        if exp_word in predicted_words:
            continue  # Already counted in direct overlap

        # Check if any synonym of exp_word is in predicted
        for key, synonyms in fashion_synonyms.items():
            if exp_word == key or exp_word in synonyms:
                # Check if any synonym appears in predicted
                if any(syn in predicted_lower for syn in [key] + synonyms):
                    synonym_matches += 1
                    break

    synonym_score = synonym_matches / expected_word_count if expected_word_count > 0 else 0.0

    # Combine scores (weighted average)
    final_score = (base_score * 0.7) + (synonym_score * 0.3)

    return min(final_score, 1.0)


def list_overlap_score(predicted: List[str], expected: List[str]) -> float:
    """
    Calculate overlap score between two lists.

    Args:
        predicted: List of predicted items
        expected: List of expected items

    Returns:
        Score between 0.0 and 1.0 based on list overlap
    """
    if not expected:
        return 0.0

    if not predicted:
        return 0.0

    predicted_set = set(item.lower().strip() for item in predicted)
    expected_set = set(item.lower().strip() for item in expected)

    intersection = predicted_set & expected_set
    precision = len(intersection) / len(predicted_set) if predicted_set else 0.0
    recall = len(intersection) / len(expected_set) if expected_set else 0.0

    # F1 score
    if precision + recall == 0:
        return 0.0

    f1 = 2 * (precision * recall) / (precision + recall)
    return f1


def calculate_accuracy(results: List[dict], threshold: float = 0.7) -> dict:
    """
    Calculate overall accuracy metrics from a list of evaluation results.

    Args:
        results: List of result dictionaries with 'score' field
        threshold: Threshold for considering a result as correct

    Returns:
        Dictionary with accuracy metrics
    """
    if not results:
        return {
            "total": 0,
            "passed": 0,
            "accuracy": 0.0,
            "avg_score": 0.0
        }

    total = len(results)
    passed = sum(1 for r in results if r.get("score", 0) >= threshold)
    avg_score = sum(r.get("score", 0) for r in results) / total

    return {
        "total": total,
        "passed": passed,
        "accuracy": passed / total,
        "avg_score": avg_score
    }


def weighted_score(scores: dict, weights: dict = None) -> float:
    """
    Calculate weighted average of multiple scores.

    Args:
        scores: Dictionary of score_name: score_value pairs
        weights: Dictionary of score_name: weight pairs (defaults to equal weights)

    Returns:
        Weighted average score
    """
    if not scores:
        return 0.0

    if weights is None:
        weights = {key: 1.0 for key in scores.keys()}

    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0

    weighted_sum = sum(scores[key] * weights.get(key, 1.0) for key in scores.keys())
    return weighted_sum / total_weight


# Export all metrics
__all__ = [
    'exact_match',
    'partial_match',
    'fashion_similarity',
    'list_overlap_score',
    'calculate_accuracy',
    'weighted_score'
]
