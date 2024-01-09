from langchain.schema import BaseRetriever, Document
import os
import cassio
from dotenv import load_dotenv
import llmutil

load_dotenv()

token=os.environ['ASTRA_DB_APPLICATION_TOKEN']
astra_db_id=os.environ['ASTRA_DB_ID']
keyspace=os.environ["ASTRA_DB_KEYSPACE"]
table=os.environ["ASTRA_DB_TABLE"]
historytable = os.environ["ASTRA_DB_HISTORY_TABLE"]

cassio.init(
    database_id=astra_db_id,
    token=token,
    keyspace=keyspace,
)

class AstraProductRetriever(BaseRetriever):

    class Config:
        arbitrary_types_allowed = True

    def get_relevant_products(self, query, topk):
        embedding = llmutil.generate_embedding(query)
        session = cassio.config.resolve_session()
        query_select_products = f"""
        SELECT product_id, item_sku, item_name, product_url, brand, category, unit_price, image, description 
        FROM {keyspace}.{table}
        ORDER BY text_embedding ANN OF {embedding}
        LIMIT {topk} """

        results = session.execute(query_select_products)

        products = results._current_rows
        return products      

    def store_chat_history(self, session_id,query, answer):
        
        session = cassio.config.resolve_session()
        query_store_chat = f"""
        INSERT INTO {keyspace}.{historytable}
        (id, msgtime, sessionid, userquery, aianswer)
        VALUES (uuid(), toTimestamp(now()), %s, %s, %s)"""

        session.execute(query_store_chat,(str(session_id), str(query),str(answer)))
        return True

    def get_relevant_documents(self, query):
        docs = []
        embedding = llmutil.generate_embedding(query)
        session = cassio.config.resolve_session()
        query_select_products = f"""
        SELECT product_id, item_sku, item_name, product_url, brand, category, unit_price, description 
        FROM {keyspace}.{table}
        ORDER BY text_embedding ANN OF {embedding}
        LIMIT 5 """
        
        results = session.execute(query_select_products)

        top_products = results._current_rows
        for r in top_products:
            docs.append(Document(
                id=r.product_id,
                page_content=r.description,
                metadata={"product_id id": r.product_id,
                           "item_sku": r.item_sku,
                           "item_name": r.item_name,
                           "product_url": r.product_url,
                           "brand": r.brand,
                           "unit_price": r.unit_price,
                           "category": r.category
                        }
            ))

        print(docs) 
        return docs