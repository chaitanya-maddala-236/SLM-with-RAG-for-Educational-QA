from __future__ import annotations

HYDE_PROMPT = "Write a short factual passage answering the question."

SLM_RAG_PROMPT = """### Instruction
Answer using ONLY the context.
If the context does not contain the answer, say:
\"I don't know.\"

Keep the answer under 3 sentences.

### Context
{context}

### Question
{question}

### Answer
"""

PARTIAL_RAG_PROMPT = """### Instruction
Use the partial context if relevant, but be explicit about uncertainty.
Keep the answer under 3 sentences.

### Context
{context}

### Question
{question}

### Answer
"""

LLM_FALLBACK_PROMPT = """### Instruction
No reliable retrieval context is available.
Answer carefully and mention uncertainty explicitly.
Keep the answer under 3 sentences.

### Question
{question}

### Answer
"""
