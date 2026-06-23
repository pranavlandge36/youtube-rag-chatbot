from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from models import model

def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text



def build_chain(retriever,prompt):
  parallel_chain = RunnableParallel({
    'context':retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
  })

  parser = StrOutputParser()

  main_chain= parallel_chain | prompt | model | parser

  return main_chain

