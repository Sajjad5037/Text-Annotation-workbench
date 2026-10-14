
import pandas as pd

from src.quality_checks import validate_annotations


def test_valid_annotation_passes():
    annotations = pd.DataFrame([
        {
            "sample_id": "S001",
            "text": "The service was excellent.",
            "sentiment_label": "Positive",
            "rationale": "The sentence expresses satisfaction.",
            "needs_review": False,
            "review_reason": "",
            "annotation_status": "Completed",
        }
    ])

    result = validate_annotations(annotations)

    assert result["valid"] is True
    assert result["errors"] == []
    assert result["total_records"] == 1


def test_invalid_sentiment_label_fails():
    annotations = pd.DataFrame([
        {
            "sample_id": "S002",
            "text": "The package arrived on Tuesday.",
            "sentiment_label": "Very Happy",
            "rationale": "The package arrived.",
            "needs_review": False,
            "review_reason": "",
            "annotation_status": "Completed",
        }
    ])

    result = validate_annotations(annotations)

    assert result["valid"] is False
    assert any(
        "invalid sentiment labels" in error
        for error in result["errors"]
    )

def test_missing_rationale_fails():
    annotations = pd.DataFrame([
        {
            "sample_id": "S003",
            "text": "The food was delicious.",
            "sentiment_label": "Positive",
            "rationale": "",
            "needs_review": False,
            "review_reason": "",
            "annotation_status": "Completed",
        }
    ])

    result = validate_annotations(annotations)

    assert result["valid"] is False
    assert any(
        "missing rationale" in error
        for error in result["errors"]
    )


def test_flagged_annotation_requires_review_reason():
    annotations = pd.DataFrame([
        {
            "sample_id": "S004",
            "text": "Well, that was something.",
            "sentiment_label": "Uncertain",
            "rationale": "The sentiment is unclear.",
            "needs_review": True,
            "review_reason": "",
            "annotation_status": "Completed",
        }
    ])

    result = validate_annotations(annotations)

    assert result["valid"] is False
    assert any(
        "no review reason" in error
        for error in result["errors"]
    )

