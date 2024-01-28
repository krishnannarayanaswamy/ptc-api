
from datamodel import Product
from astraretriever import AstraProductRetriever
from typing import List, Tuple
from operator import itemgetter

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap,RunnableParallel, RunnablePassthrough
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import format_document
from langchain.globals import set_debug
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string

def search(
    query: str,
    topk: int = 5,
) -> List[Product]:

    set_debug(True)

    retriever = AstraProductRetriever()

    products = retriever.get_relevant_products(query, topk)

    return [
        Product(
            product_id=r.product_id,
            item_sku=r.item_sku,
            item_name=r.item_name,
            product_url=r.product_url,
            brand=r.brand,
            category=r.category,
            unit_price=r.unit_price,
            image=r.image,
            description=r.description,
        )
        for r in products
    ]


def ask(
    question: str,
    session_id: str,
) -> str:
    
    retriever = AstraProductRetriever()

    previous_chat_history = retriever.get_chat_history(session_id)

    def _format_chat_history(chat_history: List[Tuple]) -> str:
        """Format chat history into a string."""
        buffer = ""
        for dialogue_turn in chat_history:
            human = "Human: " + dialogue_turn.userquery
            ai = "Assistant: " + dialogue_turn.aianswer
            buffer += "\n" + "\n".join([human, ai])
        print(buffer)
        return buffer

    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone text, in English. If Chat History is empty, just return the follow up text as the stand alone text in English.

    Chat History:
    {chat_history}
    Follow Up question: {question}
    Standalone question:"""
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)


    template = """You are a customer service of a ecommerce store for PTC Computer in Cambodia and you are assisting customer to choose the best products for him to buy.
    You will also answering frequently asked questions, such as inquiries about delivery, returns, product information, and order tracking. Include the product description and product url when responding with the list of product recommendation.Provide detailed product information, including specifications, pricing helping users make informed purchase decisions.
    Always respond in the same language as the user question. User might ask in Khmer and/or English Language.
    Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

    DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


    def _combine_documents(
        docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
    ):
        doc_strings = [format_document(doc, document_prompt) for doc in docs]
        return document_separator.join(doc_strings)

    _inputs = RunnableParallel(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: _format_chat_history(previous_chat_history)
        )
        | CONDENSE_QUESTION_PROMPT
        | ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview")
        | StrOutputParser(),
    )
    _context = {
        "context": itemgetter("standalone_question") | retriever | _combine_documents,
        "question": lambda x: x["standalone_question"],
    }
    conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | ChatOpenAI(model_name="gpt-4-0125-preview")

    aianswer = conversational_qa_chain.invoke(
        {
            "question": {question}
        }
    )

    retriever.store_chat_history(session_id, question, aianswer.content)

    return aianswer.content


def upsert(
    products
) -> str:
    
    retriever = AstraProductRetriever()

    return retriever.upsert_products(products)