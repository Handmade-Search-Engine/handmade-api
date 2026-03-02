from flask import Flask, request, jsonify
from search import or_search, and_search, get_random_site

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route('/random')
def random():
    site = get_random_site()
    response = jsonify({"url": site})
    print(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.get("/search")
def main():
    query = request.args.get('query')

    results = and_search(query)

    response = jsonify({'results': results})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')