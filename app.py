from nlp_utils import NlpUtils
import numpy as np
import logging
import logging.config
from flask import Flask, make_response, request, Response, json

from repositories.postgres_utils import PostgresUtils
from repositories.redis_utils import RedisUtils
from search_module import GoodSearchEngine
from repositories.movie_full import MovieFullRepository
from vectors_fetcher import VectorsFetcher
from os import path

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


class SearchAppRestController:
    nlp = NlpUtils
    search_engine = GoodSearchEngine
    brief_repo = RedisUtils

    def __init__(self, nlp: NlpUtils, search_engine: GoodSearchEngine, descriptions_search_engine: GoodSearchEngine, brief_repo: RedisUtils):
        self.nlp = nlp
        self.search_engine = search_engine
        self.descriptions_search_engine = descriptions_search_engine
        self.brief_repo = brief_repo
        self.logger = logging.getLogger("searchApp")

    def hello(self):
        return self.create_response(self.nlp is None)

    def new_get(self, query):
        self.logger.info("GET request with query: {0}".format(query))
        query_vector = self.nlp.sentence_to_vector(query)
        self.logger.info("Success vectorized.")

        knn = self.search_engine.get_knn(query_vector)
        self.logger.info("Got {0} movies as result".format(len(knn)))

        results = []
        entity_name = 'movie_brief'
        for movie_id in knn:
            # TODO wrap raw db entity
            results.append(self.brief_repo.get_from_redis(entity_name, movie_id))  # it's a bad practice
        return create_response({'results': results})

    def new_get_only_description(self, query):
        self.logger.info("GET by descriptions request with query: {0}".format(query))
        query_vector = self.nlp.sentence_to_vector(query)
        self.logger.info("Success vectorized.")

        knn = self.descriptions_search_engine.get_knn(query_vector)
        self.logger.info("Got {0} movies as result".format(len(knn)))

        results = []
        entity_name = 'movie_brief'
        for movie_id in knn:
            # TODO wrap raw db entity
            results.append(self.brief_repo.get_from_redis(entity_name, movie_id))  # it's a bad practice
        return create_response({'results': results})

    def new_raw_get(self, query):
        self.logger.info("GET request with query: {0}".format(query))
        query_vector = self.nlp.sentence_to_vector(query)
        self.logger.info("Success vectorized.")

        ids, distances = self.search_engine.get_knn_raw(query_vector)
        self.logger.info("Got {0} raw ids as result".format(len(ids)))

        results = []
        entity_name = 'movie_brief'
        for movie_id in ids:
            # TODO wrap raw db entity
            results.append(self.brief_repo.get_from_redis(entity_name, movie_id))  # it's a bad practice
        return create_response({'results': results})

    def create_response(self, data):
        r = Response(
            response=json.dumps(data, default=np_encoder, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
        return r


@app.route("/movie/<kp_id>", methods=['GET'])
def get_full_info(kp_id):
    # kp_id = request.args.get('kp_id')
    print(kp_id)
    repo = MovieFullRepository()
    return create_response(repo.get_by_kp_id(kp_id).to_dict())


print("loading vectors...")
vectors_fetcher = VectorsFetcher(PostgresUtils())
vectors_fetcher.fetch()
all_vectors = vectors_fetcher.get()
descriptions_vectors = vectors_fetcher.get(only_descriptions=True)
# TODO separate reviews and description
print("vectors loaded")

print("creating search engines...")
all_search_engine = GoodSearchEngine(all_vectors)
descriptions_search_engine = GoodSearchEngine(descriptions_vectors)
print("search engines created")

print("creating controller...")
controller = SearchAppRestController(NlpUtils(), all_search_engine, descriptions_search_engine, RedisUtils('127.0.0.1'))
print("controller created")


@app.route('/hello', methods=['GET'])
def hello():
    return controller.hello()


@app.route('/movie', methods=['GET'])
def new_get():
    query = request.args.get('query')
    return controller.new_get(query)


@app.route('/movie/by_descriptions', methods=['GET'])
def new_get_by_descriptions():
    query = request.args.get('query')
    return controller.new_get_only_description(query)


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


def create_response(s):
    r = app.response_class(
        response=json.dumps(s, default=np_encoder, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return r

if __name__ == '__main__':
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'config/logger.conf')
    logging.config.fileConfig(log_file_path)

    app.run(debug=True)

