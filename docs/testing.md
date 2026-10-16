# Testing & Verification Documentation

## Automated Test Suite

Unit testing is powered by `pytest`.

### Running Tests

Execute from project root:

```bash
python -m pytest
```

### Test Coverage

1. **`tests/test_nlp.py`**:
   - Clean text transformation.
   - Tokenization & stopword removal.
   - Synonym mapping (`head ache` → `headache`).
   - Feature extraction.

2. **`tests/test_recommender.py`**:
   - End-to-end recommendation flow.
   - Empty input handling.
   - Emergency keyword trigger verification.

3. **`tests/test_database.py`**:
   - Dynamic dashboard stats retrieval.
   - Medicine search SQL queries.
   - Feedback persistence.

4. **`tests/test_safety.py`**:
   - Emergency red-flag symptom detection (`chest pain`, `breathlessness`).
   - Educational disclaimer verification.
