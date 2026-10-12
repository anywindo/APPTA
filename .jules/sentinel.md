## 2025-03-09 - Sentinel: Hardcoded API Key Exposure
**Vulnerability:** A hardcoded Google API key was found in the `app.py` frontend code inside `generate_ai_summary`.
**Learning:** Storing API keys directly in the codebase is a critical security risk because anyone with access to the codebase (or public repository) can extract and use the key for their own purposes, leading to potential abuse and cost implications.
**Prevention:** Always use environment variables to store sensitive information like API keys. Pass them at runtime.
