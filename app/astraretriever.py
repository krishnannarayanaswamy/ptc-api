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

    def upsert_products(self, products):
        
        session = cassio.config.resolve_session()
        cmd_insert_product = f"""
                INSERT INTO {keyspace}.{table}
                (product_id, item_sku, item_name, tags, brand,category, unit_price, short_description, description, product_url, image, text_embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        count = 0
        for row in products:
            count += 1
            rawtext = f"Item SKU: {row['item_sku']} Item Name: {row['item_name']} Tags: {row['tags']} Short Description: {row['short_description']} Description: {row['description']} Brand: {row['brand']} Price: {row['unit_price']} Category: {row['category']}"
            embedding = llmutil.generate_embedding(rawtext)
            session.execute(cmd_insert_product, (int(row['product_id']), str(row['item_sku']), str(row['item_name']), str(row['tags']), str(row['brand']), str(row['category']), float(row['unit_price']), str(row['short_description']),str(row['description']), str(row['product_url']), str(row['image']), embedding))
            print(f""" id: {row['product_id']} record inserted or updated.""")

        return f"""Successfully Inserted or Updated {count} products."""

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