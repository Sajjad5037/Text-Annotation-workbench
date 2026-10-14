
import pandas as pd


VALID_SENTIMENT_LABELS = {
    "Positive",
    "Negative",
    "Neutral",
    "Mixed",
    "Uncertain",
}


def validate_annotations(annotations: pd.DataFrame) -> dict:
    """
    Validate an annotation dataset and return a QA summary.
    """
    required_columns = {
        "sample_id",
        "text",
        "sentiment_label",
        "rationale",
        "needs_review",
        "review_reason",
        "annotation_status",
    }

    missing_columns = required_columns - set(annotations.columns)

    if missing_columns:
        return {
            "valid": False,
            "errors": [
                f"Missing required columns: {', '.join(sorted(missing_columns))}"
            ],
            "warnings": [],
            "total_records": len(annotations),
        }

    errors = []
    warnings = []

    # Check for missing required values
    for column in ["sample_id", "text", "sentiment_label", "rationale"]:
        missing = (
            annotations[column].isna()
            | annotations[column].astype(str).str.strip().eq("")
        )

        if missing.any():
            errors.append(
                f"{int(missing.sum())} record(s) have missing {column} values."
            )

    # Check for duplicate sample IDs
    duplicate_ids = annotations["sample_id"].duplicated(keep=False)

    if duplicate_ids.any():
        warnings.append(
            f"{int(duplicate_ids.sum())} record(s) have duplicate sample IDs."
        )

    # Check sentiment labels
    invalid_labels = (
        annotations["sentiment_label"].notna()
        & ~annotations["sentiment_label"].isin(VALID_SENTIMENT_LABELS)
    )

    if invalid_labels.any():
        errors.append(
            f"{int(invalid_labels.sum())} record(s) have invalid sentiment labels."
        )

    # Check whether uncertain records are flagged for review
    uncertain = annotations["sentiment_label"].eq("Uncertain")
    needs_review = annotations["needs_review"].fillna(False).astype(bool)

    uncertain_not_flagged = uncertain & ~needs_review

    if uncertain_not_flagged.any():
        warnings.append(
            f"{int(uncertain_not_flagged.sum())} uncertain record(s) "
            "are not flagged for review."
        )

    # Check review reasons
    flagged = needs_review

    missing_review_reason = (
        annotations["review_reason"].isna()
        | annotations["review_reason"].astype(str).str.strip().eq("")
    )

    if (flagged & missing_review_reason).any():
        errors.append(
            f"{int((flagged & missing_review_reason).sum())} flagged "
            "record(s) have no review reason."
        )

    # Summarize records requiring human review
    if flagged.any():
        warnings.append(
            f"{int(flagged.sum())} record(s) require manual review."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "total_records": len(annotations),
    }
