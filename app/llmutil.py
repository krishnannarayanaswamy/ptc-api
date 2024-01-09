import os
from openai import OpenAI

openai_api_key=os.environ["OPENAI_API_KEY"]

client = OpenAI()
client.api_key = openai_api_key
def generate_embedding(text):
    model = "text-embedding-ada-002"
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding