import nlp_utils
import count
import pandas as pd
from flask import Flask, make_response, request
# from flask_restful import Api, Resource, reqparse

from search_module import SearchEngine

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# api = Api(app)
path_to_vectors = 'data/cutted_vectorized_reviews.p'
path = '/movie'


@app.route(path, methods=['GET'])
def get():
    query = request.args.get('query')
    print('QUERY', query)
    tokenized_query = ' '.join(nlp_utils.tokenize(query))
    query_vector = nlp_utils.vectorize(tokenized_query)
    global se
    knn = se.get_knn(query_vector)
    return make_response({"results": knn})


@app.route(path + '/raw', methods=['GET'])
def raw_get():
    query = request.args.get('query')
    print('QUERY', query)
    tokenized_query = ' '.join(nlp_utils.tokenize(query))
    query_vector = nlp_utils.vectorize(tokenized_query)
    titles, distances = se.get_knn_raw(query_vector)
    results = []
    for i in range(len(titles)):
        results.append({
            'title': titles[i],
            'distance': str(distances[i])
        })
    return make_response({'row_results': results})


@app.route('/', methods=['GET'])
def hello():
    return make_response('hello!')


if __name__ == '__main__':
    global se
    se = SearchEngine(path_to_vectors)
    app.run(debug=True)
