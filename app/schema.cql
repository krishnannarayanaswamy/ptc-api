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


desc products: 

CREATE KEYSPACE products WITH replication = {'class': 'NetworkTopologyStrategy', 'ap-south-1': '3'}  AND durable_writes = true;

CREATE TABLE products.chat_history (
    id uuid PRIMARY KEY,
    aianswer text,
    msgtime timestamp,
    sessionid text,
    userquery text
) WITH additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.UnifiedCompactionStrategy'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE TABLE products.ptc_inventory (
    product_id int PRIMARY KEY,
    brand text,
    category text,
    description text,
    image text,
    image_embedding vector<float, 1536>,
    item_name text,
    item_sku text,
    product_url text,
    short_description text,
    tags text,
    text_embedding vector<float, 1536>,
    unit_price float
) WITH additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.UnifiedCompactionStrategy'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';
CREATE CUSTOM INDEX brand_index ON products.ptc_inventory (brand) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex' WITH OPTIONS = {'index_analyzer': '{"tokenizer" : {"name" : "standard"},
            "filters" : [{"name" : "porterstem"}]}'};
CREATE CUSTOM INDEX image_embedding_index ON products.ptc_inventory (image_embedding) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex' WITH OPTIONS = {'similarity_function': 'dot_product'};
CREATE CUSTOM INDEX text_embedding_index ON products.ptc_inventory (text_embedding) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex' WITH OPTIONS = {'similarity_function': 'dot_product'};