# Text Annotation Workbench
## User Manual

**Version:** 1.0  
**Application:** English Sentiment Annotation and Quality Assurance Workbench

---

## 1. Introduction

The Text Annotation Workbench is an interactive application for labeling English text according to its sentiment. It allows users to assign sentiment labels, document their decisions, flag ambiguous examples for review, validate annotations, monitor progress, and export annotated data as a CSV file.

The application is designed to demonstrate a structured text annotation workflow.

### Key features

- Explore and search the sample dataset.
- Filter samples by annotation status.
- Assign sentiment labels and provide rationales.
- Flag samples for manual review.
- Follow annotation guidelines and examples.
- Monitor annotation progress and label distribution.
- Run automated quality checks.
- Export saved annotations to CSV.

## 2. Getting Started

Open the Text Annotation Workbench in your browser.

If you are running the application locally, open a terminal in the project folder, activate the Python virtual environment, and run:

```bash
python -m streamlit run app.py
```

Then open the local address displayed in the terminal, usually `http://localhost:8501`.

## 3. Exploring the Dataset

The **Dataset Explorer** section allows users to inspect the available sample texts before annotating them.

### 3.1 View the dataset

1. Expand **Explore the sample dataset**.
2. Review the total number of samples.
3. Inspect the sample IDs and text in the dataset table.
4. Review the annotation progress bar and sentiment distribution chart.

The progress bar shows the number of samples annotated during the current application session. The sentiment distribution chart summarizes the labels assigned to saved annotations.

### 3.2 Search for text

1. Locate the **Search sample text** field.
2. Enter a word or phrase.
3. Review the matching samples.

The search is case-insensitive and supports searching for words or phrases within the sample text.

For example, searching for `service` returns samples containing that word, regardless of capitalization.

Clear the search field to display results without the text-search restriction.

### 3.3 Filter by annotation status

Use **Filter samples by annotation status** to select one of the following options:

- **All samples:** Displays the complete dataset.
- **Not annotated:** Displays samples that have not been annotated.
- **Completed:** Displays samples with saved annotations marked as completed.
- **Needs review:** Displays samples flagged for manual review.

The text search and status filter can be used together. For example, selecting **Completed** and searching for `service` displays completed samples whose text contains that term.

## 4. Understanding the Annotation Guidelines

Before annotating a sample, review the **Annotation Guidelines** section.

The application uses five sentiment labels.

| Label | When to use it |
|---|---|
| Positive | The text expresses satisfaction, praise, or a favorable opinion. |
| Negative | The text expresses dissatisfaction, criticism, or an unfavorable opinion. |
| Neutral | The text provides factual or informational content without clear positive or negative sentiment. |
| Mixed | The text contains both positive and negative sentiment. |
| Uncertain | The sentiment cannot be determined confidently from the available text. |

### Example annotations

- **Positive:** “The service was excellent.”
- **Negative:** “The product stopped working.”
- **Neutral:** “The appointment is on Friday.”
- **Mixed:** “The food was delicious, but the service was terrible.”
- **Uncertain:** “Well, that was something.”

These examples illustrate the intended use of each label. Always consider the available context before making a decision.

### Good annotation practices

- Base your decision on the text rather than unsupported assumptions about the author.
- Consider contrast and apparent sarcasm.
- Provide a rationale that explains your decision.
- Flag ambiguous or difficult samples for manual review.

## 5. Annotating a Sample

The **Annotate Text** section is where users assign labels to individual samples.

### Step 1: Review the sample

Read the displayed text carefully. Check the sample number and sample ID so you know which record you are annotating.

### Step 2: Select a sentiment label

Use the **Sentiment label** dropdown to select one of the five sentiment categories.

A label must be selected before the annotation can be saved.

### Step 3: Enter an annotation rationale

In the **Annotation rationale** field, explain why the selected label fits the text.

For example:

Text: “The service was excellent.”

Label: Positive

Rationale: “The text expresses clear satisfaction with the service.”

The rationale should explain the linguistic evidence supporting your decision rather than simply repeat the selected label.

### Step 4: Flag the sample for review when necessary

Check **Flag this sample for review** if the sample is ambiguous, difficult to interpret, or requires further assessment.

If the review flag is selected, enter an explanation in **Review reason (if applicable)**.

For example:

- Review flag: Selected
- Review reason: “The intended sentiment is unclear without additional context.”

The application requires a review reason when a sample is flagged for review.

An on-screen reminder also encourages users to consider review when they select the Uncertain label without enabling the review flag.

### Step 5: Save the annotation

Click **Save Annotation**.

The application checks that:
- A sentiment label has been selected.
- A rationale has been provided.
- A review reason has been entered if the sample is flagged for review.

If these checks pass, the annotation is saved for the current session, and the application refreshes.

## 6. Navigating Between Samples

The **Sample Navigation** section provides three ways to move through the dataset.

- **Previous:** Moves to the preceding sample.
- **Go to sample:** Opens a selected sample using its ID and text.
- **Next:** Moves to the following sample.

The Previous button is disabled at the first sample, and the Next button is disabled at the last sample.

When you revisit a sample that has already been annotated, the application loads its saved annotation values into the form. You can update the label, rationale, or review information and save the changes.

## 7. Monitoring Annotation Progress

The application provides an overview of annotation activity.

### 7.1 Annotation Overview

This section displays:
- Total Samples
- Completed
- Needs Review

These metrics help users understand how many records have been processed and how many require additional attention.

### 7.2 Progress bar

The progress bar in Dataset Explorer indicates the number of samples with saved annotations relative to the total dataset size.

For example, if 4 of 20 samples are annotated, the progress is 20%.

### 7.3 Sentiment Label Distribution

The chart displays the distribution of sentiment labels among the saved annotations.

Only labels with at least one saved annotation are displayed. The chart updates as annotations are added or changed.

This chart describes the annotations made so far; it does not represent pre-existing sentiment labels for the entire dataset.

## 8. Reviewing Saved Annotations

The **Saved Annotations** section displays the annotations recorded during the current session.

The table includes fields such as:
- Sample ID
- Text
- Sentiment label
- Rationale
- Review status
- Review reason
- Annotation status

Review this table to verify that your labels and explanations have been recorded as intended.

## 9. Quality Assurance

The **Quality Assurance** section runs structural validation checks on the saved annotations.

It displays:
- **Records Checked:** Number of annotation records checked.
- **Errors:** Number of validation error messages.
- **Warnings:** Number of validation warning messages.

### Examples of validation checks

The application checks for:
- Missing required fields.
- Invalid sentiment labels.
- Duplicate sample IDs.
- Uncertain labels without a review flag.
- Review flags without a review reason.

Some findings are treated as errors, while others are warnings. For example, an uncertain annotation without a review flag produces a warning rather than automatically invalidating the annotation.

A message indicating that no structural validation errors were found means the records passed the implemented checks. It does not guarantee that every sentiment label or rationale is linguistically correct. Human review may still be necessary.

## 10. Exporting Annotations

Users can export their saved annotations for further analysis or processing.

### Export procedure

1. Complete and save the annotations you want to export.
2. Navigate to **Saved Annotations**.
3. Click **Download Annotations (CSV)**.
4. Save the downloaded file.
5. Open it in a spreadsheet application or process it using Python.

The exported CSV contains the saved annotation records, including their labels, rationales, review information, and status.

Before sharing the file, check that the exported records are complete and that the review flags and reasons have been recorded correctly.

## 11. Important Limitations

This version is a demonstration application with a small sample dataset.

- **Session-based storage:** Annotations are stored in Streamlit session state, not in a permanent database. They may be lost when the session resets. Export your work before ending the session.
- **Sample dataset:** The application currently uses 20 English text examples.
- **Sentiment scope:** The available labels are intended for English sentiment annotation.
- **Structural quality checks:** The validation logic checks defined data-quality rules; it does not independently establish linguistic accuracy.
- **No multi-user workflow:** The current version does not provide a shared database, user accounts, or collaborative annotation management.
- **No inter-annotator agreement measurement:** The application does not currently calculate agreement between multiple annotators.

## 12. Recommended Workflow

For a typical annotation session, follow this sequence:

1. Explore the dataset and read the annotation guidelines.
2. Select a sample using Sample Navigation.
3. Read the text and select the appropriate sentiment label.
4. Enter a clear rationale.
5. Flag ambiguous samples for review and provide a review reason.
6. Save the annotation.
7. Repeat for additional samples.
8. Review annotation progress and label distribution.
9. Check the Quality Assurance results.
10. Export the saved annotations as a CSV file.
11. Verify the exported file before sharing or using it elsewhere.

---

**End of User Manual**

Text Annotation Workbench — Version 1.0