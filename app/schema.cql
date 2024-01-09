CREATE TABLE IF NOT EXISTS {keyspace}.{table}
(product_id int,
 item_sku text,
 item_name text,
 tags text,
 brand text,
 category text,
 unit_price float,
 short_description text,
 description text,
 product_url text,
 image text,
 text_embedding vector<float, 1536>,
 image_embedding vector<float, 1536>,
 PRIMARY KEY (product_id));

CREATE CUSTOM INDEX IF NOT EXISTS text_embedding_index ON {keyspace}.{table}(text_embedding)
USING 'org.apache.cassandra.index.sai.StorageAttachedIndex' WITH OPTIONS = {{ 'similarity_function': 'dot_product' }};

CREATE CUSTOM INDEX IF NOT EXISTS image_embedding_index ON {keyspace}.{table}(image_embedding)
USING 'org.apache.cassandra.index.sai.StorageAttachedIndex' WITH OPTIONS = {{ 'similarity_function': 'dot_product' }};

CREATE CUSTOM INDEX IF NOT EXISTS brand_index ON {keyspace}.{table}(brand)
USING 'org.apache.cassandra.index.sai.StorageAttachedIndex' WITH OPTIONS = {{ 'index_analyzer': '{{"tokenizer" : {{"name" : "standard"}},
"filters" : [{{"name" : "porterstem"}}]}}'}};


CREATE TABLE IF NOT EXISTS {keyspace}.{table}
(id uuid,
 sessionid text,
 msgtime timestamp,
 userquery text,
 aianswer text,
 PRIMARY KEY (id));


 INSERT INTO {keyspace}.{table}
                (id, msgtime, sessionid, userquery, aianswer)
                VALUES (%s, %s, %s, %s, %s)