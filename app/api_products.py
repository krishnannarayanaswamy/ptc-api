
from datamodel import Product
from astraretriever import AstraProductRetriever
from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough

def search(
    query: str,
    topk: int = 5,
) -> List[Product]:

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
    query: str,
    session_id: str,
) -> str:
    
    retriever = AstraProductRetriever()

    template = """You are a customer service of a ecommerce store and you are assisting customer to choose the best products for him to buy.
    Be nice to the customer. Greet them, when required and be polite.
    You will also answering frequently asked questions, such as inquiries about delivery, returns, product information, and order tracking 
    Include the product description and product url when responding with the list of product recommendation.
    Provide detailed product information, including specifications, pricing, availability, and customer reviews, helping users make informed purchase decisions.
    All the responses should be the same language as the user used. Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(model="gpt-3.5-turbo")
    output_parser = StrOutputParser()

    setup_and_retrieval = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    )
    chain = setup_and_retrieval | prompt | model | output_parser

    aianswer = chain.invoke(query)

    retriever.store_chat_history(session_id, query, aianswer)

    return aianswer


def update(
    products
) -> str:
    


    return ""