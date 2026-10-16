# Natural Language Processing (NLP) Methodology

## Objectives

The NLP module (`src/nlp_processor.py`) cleans and transforms free-form user symptom text into standardized canonical symptom tokens present in our medical database dictionary.

## Preprocessing Pipeline

```
Raw User Text ("I have head ache, temperature and body pain")
   │
   ▼ Lowercasing & Punctuation Stripping
("i have head ache temperature and body pain")
   │
   ▼ Synonym Mapping
("i have headache fever and body pain")
   │
   ▼ Tokenization & Stopword Removal
["headache", "fever", "body", "pain"]
   │
   ▼ Symptom Dictionary Extraction
["fever", "headache", "body pain"]
```

## Step-by-Step Techniques

1. **Lowercasing & Cleaning**: Standardizes case and strips special characters to avoid mismatch.
2. **Stopword Removal**: Removes non-informative words (`"i"`, `"have"`, `"and"`, `"suffering"`, `"from"`).
3. **Synonym Normalization**:
   - `"head ache"` → `"headache"`
   - `"temperature"` → `"fever"`
   - `"stomach ache"` → `"stomach pain"`
   - `"coughing"` → `"cough"`
4. **Keyword & N-Gram Extraction**: Matches exact multi-word and single-word symptom strings against database symptom records.
