from langchain_core.prompts import PromptTemplate

prompts =PromptTemplate(
    template="""
You are a YouTube video assistant.

Use ONLY the transcript context below.

If the answer cannot be found in the transcript,
respond exactly:

"I don't know based on the transcript."

Transcript:
{context}

Question:
{question}

Answer:
""",
    input_variables=['context','question']

)
