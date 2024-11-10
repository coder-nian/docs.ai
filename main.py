import os
import argparse
from groq import Groq
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from embedding_functions import embedding_api, embedding_llm

client = Groq(
    api_key=os.environ.get("RAG_API_KEY"),
)

instructions = (
    "You're an AI chatbot named Docs.AI."
    "Maintain a professional and friendly tone."
    "Provide as much information as possible."
    "Answer any follow-up questions for clarification."
    "Aim to provide comprehensive information in your responses."
)
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    history = []
    print(f"Response: {query_api(args.query_text, history)}")


def search_db(query_text: str):
    # Prepare the DB.
    embedding_function = embedding_api()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    return prompt_template.format(context=context_text, question=query_text)


# Querying the llm using API
def query_api(query_text: str, history: list):
    prompt = search_db(query_text)
    if not history:
        history.append(
            {
                "role": "assistant",
                "content": instructions
            }
        )
    history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    chat_completion = client.chat.completions.create(
        messages=history,
        model="llama-3.1-70b-versatile",
    )
    response = chat_completion.choices[0].message.content
    history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    return response


# Querying the local llm
def query_llm(query_text: str, history: list):
    prompt = search_db(query_text)
    if not history:
        history.append(
            {
                "role": "assistant",
                "content": instructions
            }
        )
    history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    model = Ollama(model="llama3.1")
    response = model.invoke(prompt)
    history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    return response


if __name__ == "__main__":
    main()
