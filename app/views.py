#import logging
#from app import app
from flask import Flask,render_template, request
from api_products import search, ask
import json

app = Flask(__name__)

@app.route('/')
def home():
   return "Welcome to PTC AI Assistant APIs!"

@app.route('/info')
def template():
    return render_template('home.html')

@app.route("/search_products", methods=["POST"])
def search_products():
    data = request.get_json()
    print(f"Data recieved: {data}")
    query = data.get("query")
    topk = data.get("topk", 5)

    results = search(
        query=query,
        topk=topk,
    )

    response = {"results": [r.to_dict() for r in results]}
    print(f"Results recieved: {response}")
    return response, 200

@app.route("/ask_ai_assistant", methods=["POST"])
def ask_ai_assistant():
    data = request.get_json()
    print(f"Data recieved: {data}")
    query = data.get("query")
    session_id = data.get("session_id", "")

    response = ask(
        query=query,
        session_id=session_id,
    )

    print(f"Results recieved: {response}")
    return response, 200

@app.route("/update_inventory", methods=["POST"])
def update_inventory():
    data = request.get()
    products = json.loads(data.text)
    print(f"Data recieved: {products}")

    for product in products:
        print(product['product_id'])

    response = ask(
        products=products,
    )

    print(f"Results recieved: {response}")
    return response, 200

# main driver function
if __name__ == "__main__":
    app.run()



