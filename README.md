# my-gemini-requestor

A Python utility class to prompt **Gemini API** to convert a document (unstructured data) into equivalent JSON data (structured).

This is part of my larger end-to-end personal finance tracking project.

## 📌 Overview

```mermaid
graph LR
    A[Prompt + Document] --> B[Gemini API] --> C[JSON Output]
```

## How to use

```python
from pathlib import Path
from my_gemini_requestor import GeminiRequestor

# Define your prompt and document
prompt = "Extract the transaction date, merchant, and amount from this receipt."
file_path = Path("path/to/your/document.pdf")

# Create the requestor
requestor = GeminiRequestor(prompt=prompt, file_path=file_path)

# Get response data
print(requestor.response)
# [
#   {
#     "transaction_date": "2025-04-20",
#     "merchant": "Vendor",
#     "amount": 420        
#   }
# ]
```