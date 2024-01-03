from flask import Flask, jsonify, request
from rag_opt import generate_context
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
VALIDATION_TOKEN = os.getenv("VALIDATION_TOKEN")

@app.route("/checkAPI",methods=["POST","GET"])
def check_server():
    response = {"result":"Live"}
    return jsonify(response),200


@app.route("/generatecontext",methods=["POST","GET"])
def gen_context():
    validation_token = request.headers.get("VALIDATION-TOKEN")

    if validation_token!=VALIDATION_TOKEN:
        return jsonify({"Error":"Incorrect Validation Token"}), 400
    
    data = request.get_json()

    if "input_query" not in data:
        return jsonify({"Error":"Missing input_query paramter in request"}),400
    
    query = data["input_query"]
    context = generate_context(query=query)
    
    return jsonify({"result":str(context)}),200


if __name__ == "__main__":
    app.run(port=6000,debug=True)
