from src.blockchain import Blockchain
from textwrap import dedent
from uuid import uuid4

from flask import Flask, jsonify, request

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route("/transaction/new", methods=["POST"])
def new_transaction():
    values = request.get_json()

    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    index = blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])

    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route("/mine", methods=["GET"])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction("0", node_identifier, 1)

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash=previous_hash)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transaction": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return jsonify(response), 200


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json()

    nodes = values.get("nodes")
    if nodes is None:
        return "Error: not a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        "message": "New nodes added",
        "total_nodes": list(blockchain.nodes)
    }

    return jsonify(response), 201

@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            "message": "Our chain was replaced",
            "new_chain": blockchain.chain
        }

    else:
        response = {
            "message": "Our chain is authoratative",
            "chain": blockchain.chain
        }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



