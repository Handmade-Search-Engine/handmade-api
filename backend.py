from flask import Flask, request, jsonify
from search import search

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.get("/search")
def main():
    query = request.args.get('query')

    results = search(query)

    response = jsonify({'results': results})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')