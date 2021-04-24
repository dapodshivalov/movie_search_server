import nlp_utils
import count
import pandas as pd
import logging
from flask import Flask, make_response, request

from search_module import SearchEngine

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# api = Api(app)
path_to_vectors = 'data/cutted_vectorized_reviews.p'
path = '/movie'


@app.route(path, methods=['GET'])
def get():
    log = logging.getLogger('file')
    query = request.args.get('query')
    print('QUERY', query)
    log.debug('QUERY' + query)

    tokenized_query = ' '.join(nlp_utils.tokenize(query))
    query_vector = nlp_utils.vectorize(tokenized_query)
    log.debug('Vector: ' + str(query_vector))
    global se
    knn = se.get_knn(query_vector)
    log.debug('RESULT')
    log.debug(str(knn))
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
    logging.basicConfig(filename="application.log", level=logging.DEBUG)
    app.run(debug=True)
