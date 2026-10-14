
from pathlib import Path

import pandas as pd
import streamlit as st
from src.quality_checks import validate_annotations

# Page configuration
st.set_page_config(
    page_title="Text Annotation Workbench",
    page_icon="📝",
    layout="wide",
)


# Load sample dataset
DATA_PATH = Path(__file__).parent / "data" / "sample_dataset.csv"
df = pd.read_csv(DATA_PATH)


# Initialize annotation storage for the current session
if "annotations" not in st.session_state:
    st.session_state.annotations = {}

if "current_sample" not in st.session_state:
    st.session_state.current_sample = 0


# Page header
st.title("Text Annotation Workbench")

st.write(
    "An interactive demonstration of NLP text annotation "
    "and quality assurance."
)

st.info(
    "Our goal: annotate text consistently, explain labeling "
    "decisions, and validate annotation quality."
)

st.subheader("Dataset Explorer")

with st.expander("Explore the sample dataset", expanded=False):
    st.write(f"**Number of samples:** {len(df)}")
    
    completed_count = len(st.session_state.annotations)
    total_count = len(df)
    progress = completed_count / total_count if total_count else 0

    st.write(
        f"**Annotation progress:** {completed_count} of {total_count} samples completed"
    )
    st.progress(progress)
    
    st.write("**Sentiment Label Distribution**")

    if st.session_state.annotations:
        annotation_df = pd.DataFrame(
            list(st.session_state.annotations.values())
        )

        label_counts = (
            annotation_df["sentiment_label"]
            .value_counts()
            .reindex(
                ["Positive", "Negative", "Neutral", "Mixed", "Uncertain"],
                fill_value=0,
            )
        )

        nonzero_label_counts = label_counts[label_counts > 0]

        if not nonzero_label_counts.empty:
            st.bar_chart(nonzero_label_counts, horizontal=True)
        else:
            st.info("No sentiment labels have been assigned yet.")
    else:
        st.info("Save your first annotation to see the sentiment distribution.")


    st.write(f"**Dataset columns:** {', '.join(df.columns)}")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )
    status_filter = st.selectbox(
        "Filter samples by annotation status",
        options=[
            "All samples",
            "Not annotated",
            "Completed",
            "Needs review",
        ],
        key="dataset_status_filter",
    )

    search_text = st.text_input(
        "Search sample text",
        placeholder="Enter a word or phrase...",
        key="dataset_search",
    )

    
    # Start with all samples
    filtered_df = df.copy()

    # Apply annotation status filter
    annotations = st.session_state.annotations

    if status_filter == "Not annotated":
        annotated_ids = set(annotations.keys())
        filtered_df = filtered_df[
            ~filtered_df["sample_id"].isin(annotated_ids)
        ]

    elif status_filter == "Completed":
        completed_ids = {
            sample_id
            for sample_id, annotation in annotations.items()
            if annotation["annotation_status"] == "Completed"
        }
        filtered_df = filtered_df[
            filtered_df["sample_id"].isin(completed_ids)
        ]

    elif status_filter == "Needs review":
        review_ids = {
            sample_id
            for sample_id, annotation in annotations.items()
            if annotation["needs_review"]
        }
        filtered_df = filtered_df[
            filtered_df["sample_id"].isin(review_ids)
        ]

    # Apply text search to the filtered results
    if search_text.strip():
        filtered_df = filtered_df[
            filtered_df["text"].str.contains(
                search_text.strip(),
                case=False,
                na=False,
                regex=False,
            )
        ]

    st.write(f"**Matching samples:** {len(filtered_df)}")
    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True,
    )



# Annotation overview
st.subheader("Annotation Overview")

annotations = st.session_state.annotations

completed_count = len(annotations)
review_count = sum(
    1
    for annotation in annotations.values()
    if annotation["needs_review"]
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Samples", len(df))
col2.metric("Completed", completed_count)
col3.metric("Needs Review", review_count)

st.caption("Demo version 1.0 · English Sentiment Annotation")


# Annotation form
st.divider()

st.subheader("Annotation Guidelines")

with st.expander("View sentiment labeling rules", expanded=False):
    st.markdown("""
    - **Positive:** The text expresses satisfaction, praise, or a favorable opinion.
    - **Negative:** The text expresses dissatisfaction, criticism, or an unfavorable opinion.
    - **Neutral:** The text is factual or informational, without a clear positive or negative sentiment.
    - **Mixed:** The text contains both positive and negative sentiment.
    - **Uncertain:** The sentiment cannot be determined confidently from the available text.

    **Guidance for annotators**
    - Base labels on the text, not assumptions about the author.
    - Consider context, contrast, and sarcasm where apparent.
    - Use the rationale field to explain the labeling decision.
    - Flag ambiguous or difficult examples for manual review.
    """)

with st.expander("View example annotations", expanded=False):
    st.markdown("""
    | Sentiment | Example text | Why |
    |---|---|---|
    | Positive | "The service was excellent." | Clear praise |
    | Negative | "The product stopped working." | Clear dissatisfaction |
    | Neutral | "The appointment is on Friday." | Factual information |
    | Mixed | "The food was delicious, but the service was terrible." | Both positive and negative sentiment |
    | Uncertain | "Well, that was something." | Meaning is ambiguous without more context |
    """)


st.subheader("Annotate Text")

sample_index = st.session_state.current_sample
sample = df.iloc[sample_index]
sample_id = sample["sample_id"]

st.caption(
    f"Sample {sample_index + 1} of {len(df)} · ID: {sample_id}"
)

st.markdown("**Text to annotate**")
st.info(sample["text"])

existing = annotations.get(sample_id, {})

labels = [
    "Select a label",
    "Positive",
    "Negative",
    "Neutral",
    "Mixed",
    "Uncertain",
]

with st.form(key=f"annotation_form_{sample_id}"):
    sentiment = st.selectbox(
        "Sentiment label",
        options=labels,
        index=(
            labels.index(existing["sentiment_label"])
            if existing.get("sentiment_label") in labels
            else 0
        ),
    )

    rationale = st.text_area(
        "Annotation rationale",
        value=existing.get("rationale", ""),
        placeholder="Explain why this label fits the text...",
    )

    needs_review = st.checkbox(
        "Flag this sample for review",
        value=existing.get("needs_review", False),
    )

    review_reason = st.text_input(
        "Review reason (if applicable)",
        value=existing.get("review_reason", ""),
        placeholder="Explain why this sample needs review...",
    )
    
    


    submitted = st.form_submit_button("Save Annotation")

    if submitted:
        if sentiment == "Select a label":
            st.error("Please select a sentiment label.")

        elif len(rationale.strip()) < 10:
            st.error(
                "Please provide a more detailed rationale "
                "(at least 10 characters)."
            )

        elif needs_review and not review_reason.strip():
            st.error("Please explain why this sample needs review.")

        else:
            annotations[sample_id] = {
                "sample_id": sample_id,
                "text": sample["text"],
                "sentiment_label": sentiment,
                "rationale": rationale.strip(),
                "needs_review": needs_review,
                "review_reason": review_reason.strip(),
                "annotation_status": "Completed",
            }

            st.session_state.annotations = annotations

            st.success(f"Annotation saved for {sample_id}.")
            st.rerun()


if sentiment == "Uncertain" and not needs_review:
    st.caption(
        "Tip: Consider flagging uncertain examples for manual review."
    )

# Sample navigation
st.divider()
st.subheader("Sample Navigation")

nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col1:
    if st.button(
        "← Previous",
        disabled=sample_index == 0,
        width="stretch",
    ):
        st.session_state.current_sample -= 1
        st.rerun()

with nav_col2:
    st.selectbox(
        "Go to sample",
        options=list(range(len(df))),
        format_func=lambda i: (
            f"{df.iloc[i]['sample_id']} — "
            f"{str(df.iloc[i]['text'])[:45]}"
        ),
        index=sample_index,
        key="sample_selector",
        on_change=lambda: setattr(
            st.session_state,
            "current_sample",
            st.session_state.sample_selector,
        ),
    )

with nav_col3:
    if st.button(
        "Next →",
        disabled=sample_index == len(df) - 1,
        width="stretch",
    ):
        st.session_state.current_sample += 1
        st.rerun()


# Saved annotations and CSV export
if annotations:
    st.divider()
    st.subheader("Saved Annotations")

    annotation_df = pd.DataFrame(list(annotations.values()))

    st.dataframe(
        annotation_df,
        width="stretch",
        hide_index=True,
    )

    csv_data = annotation_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Download Annotations (CSV)",
        data=csv_data,
        file_name="annotated_dataset.csv",
        mime="text/csv",
    )

    st.caption(
        f"{len(annotation_df)} annotation(s) ready for export."
    )

else:
    st.info(
        "No annotations saved yet. Annotate a sample to enable CSV export."
    )


# Quality Assurance
st.divider()
st.subheader("Quality Assurance")

if annotations:
    annotation_df = pd.DataFrame(list(annotations.values()))

    qa_result = validate_annotations(annotation_df)

    if qa_result["valid"]:
        st.success("No structural validation errors found.")
    else:
        st.error("Validation errors detected.")

    qa_col1, qa_col2, qa_col3 = st.columns(3)

    qa_col1.metric("Records Checked", qa_result["total_records"])
    qa_col2.metric("Errors", len(qa_result["errors"]))
    qa_col3.metric("Warnings", len(qa_result["warnings"]))

    if qa_result["errors"]:
        st.markdown("**Errors**")
        for error in qa_result["errors"]:
            st.error(error)

    if qa_result["warnings"]:
        st.markdown("**Warnings**")
        for warning in qa_result["warnings"]:
            st.warning(warning)

else:
    st.info("Save an annotation to run quality checks.")

