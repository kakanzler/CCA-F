# Exercise 3: Build a Structured Data Extraction Pipeline

## Objective:

- Practice designing JSON schemas, using `tool_use` for structured output, implementing **validation-retry loops**, and designing **batch processing** strategies.

## Steps:

- Define an *extraction tool* with a JSON schema containing required and optional fields, an enum with an *"other" + detail string pattern*, and nullable fields for information that may not exist in source documents. Process documents where some fields are absent and verify the model returns null rather than fabricating values.

- Implement a **validation-retry loop**: when Pydantic or JSON schema validation fails, send a follow-up request including the document, the failed extraction, and the specific validation error. Track which errors are resolvable via retry (format mismatches) versus which are not (information absent from source).

- Add *few-shot examples* demonstrating extraction from documents with varied formats (e.g., inline citations vs bibliographies, narrative descriptions vs structured tables) and verify improved handling of structural variety.

- Design a **batch processing strategy**: submit a batch of 100 documents using the Message BatchesAPI, handle failures by custom_id, resubmit failed documents with modifications (e.g., chunking oversized documents), and calculate total processing time relative to SLA constraints.

- Implement **a human review routing strategy**: have the model output field-level confidence scores,route low-confidence extractions to human review, and analyze accuracy by document type and field to verify consistent performance.

## Domains reinforced:

- Domain 4 (Prompt Engineering & Structured Output), Domain 5 (ContextManagement & Reliability)
