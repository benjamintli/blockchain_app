# BlockChain Tutorial

## Instructions
```
$ flask run --port 5000
$ flask run --port 5001
```
Send GET requests to `/mine` endpoint to mine a block, POST to `transaction/new` to make a new transaction

Send POST requests to `127.0.0.1:5000/nodes/register` with:
```
{
    "nodes": ["https://127.0.0.1:5001"]
}
```
To register new node

Resolve chains, GET request to `nodes/resolve`