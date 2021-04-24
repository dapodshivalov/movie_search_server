import nlp_utils
import count
import pandas as pd
import logging
from flask import Flask, make_response, request, Response

from search_module import SearchEngine

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# api = Api(app)
path_to_vectors = 'data/cutted_vectorized_reviews.p'
path = '/movie'

global se
se = SearchEngine(path_to_vectors)
logging.basicConfig(filename="application.log", level=logging.DEBUG)


@app.route(path, methods=['GET'])
def get():
    log = logging.getLogger('file')
    query = request.args.get('query')
    print('QUERY', query)
    log.debug('QUERY ' + query)
    tokenized_query = ' '.join(nlp_utils.tokenize(query))
    query_vector = nlp_utils.vectorize(tokenized_query)
    log.debug('Vector: ' + str(query_vector))
    global se
    knn = se.get_knn(query_vector)
    log.debug('RESULT')
    log.debug(str(knn))
    return create_response(str({'results': knn}))


@app.route(path + '/raw', methods=['GET'])
def raw_get():
    log = logging.getLogger('file')
    query = request.args.get('query')
    print('QUERY', query)
    log.debug('QUERY ' + query)
    tokenized_query = ' '.join(nlp_utils.tokenize(query))
    query_vector = nlp_utils.vectorize(tokenized_query)
    titles, distances = se.get_knn_raw(query_vector)
    results = []
    for i in range(len(titles)):
        results.append({
            'title': titles[i],
            'distance': str(distances[i])
        })
    return create_response(str({'row_results': results}))


@app.route('/', methods=['GET'])
def hello():
    print("hello log!")
    return create_response("Привет!")


def create_response(s):
    r = Response(response=s, status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r

if __name__ == '__main__':
    app.run(debug=True)
