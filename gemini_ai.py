from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def GenminiAI(context, user_input):
    Prompt_template = """
                    Answer the question based only one the following context:
                    {context}
                    Answer the question based on the above context: {question}.
                    Provide a detailed answer.
                    Don't justify your answers.
                    Don't get information not mentioned in the CONTEXT INFORMATION.
                    Do not say "according to the context" or "mentioned in the context" or
                    similar
                    """
    pt = ChatPromptTemplate.from_template(Prompt_template)
    
    API_KEY = open('.genimi.txt').read().strip()
    model = ChatGoogleGenerativeAI(api_key=API_KEY, model='gemini-2.0-flash-exp')
    parser = StrOutputParser()
    
    rag_chain = {"context": context | format_docs, "question": RunnablePassthrough()} | pt | model | parser
    ai_response = rag_chain.invoke(user_input)
    return ai_response