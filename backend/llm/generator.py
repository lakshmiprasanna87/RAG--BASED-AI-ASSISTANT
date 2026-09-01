import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set in the .env file")

client = Groq(api_key=api_key)


def generate_answer(question, retrieved_documents, language="English"):

    # Convert retrieved documents into context
    context_parts = []

    for doc in retrieved_documents:
        if hasattr(doc, "page_content"):
            context_parts.append(doc.page_content)

        elif isinstance(doc, dict):
            context_parts.append(
                doc.get("page_content")
                or doc.get("text")
                or doc.get("content")
                or str(doc)
            )

        else:
            context_parts.append(str(doc))

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are IP-SAKTI Sahayak, a multilingual AI assistant
for Intellectual Property and Ayurveda regulatory guidance.

Answer the user's question using the retrieved PDF information.

User question:
{question}

Selected language:
{language}

Instructions:
- Answer in {language}.
- Use the retrieved PDF information as the source.
- Do not invent information.
- If the retrieved documents do not contain enough information,
  clearly say that the information is not available in the provided documents.
- Preserve important IP and Ayurveda technical terms.
- Give a clear and understandable answer.

Retrieved information:
{retrieved_documents}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are an accurate IP and regulatory information assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    sources = []

    for doc in retrieved_documents:
        if hasattr(doc, "metadata"):
            metadata = doc.metadata or {}

            source = (
                metadata.get("source")
                or metadata.get("file_name")
                or metadata.get("filename")
            )

            if source and source not in sources:
                sources.append(source)

        elif isinstance(doc, dict):
            source = (
                doc.get("source")
                or doc.get("file_name")
                or doc.get("filename")
            )

            if source and source not in sources:
                sources.append(source)

    return {
        "answer": answer,
        "sources": sources
    }