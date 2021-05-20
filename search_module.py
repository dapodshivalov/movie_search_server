import pandas as pd
import nmslib
import numpy
# from count import count


class GoodSearchEngine:
    def __init__(self, movie_id_and_vector_pairs: [dict]):
        """
        SearchEngine Constructor
        :param movie_id_and_vector_pairs: `list` of `dict`,
            elements have to contain `movie_id` and `vector` keys, like {'movie_id': movie_id, 'vector': [float]}
        """
        self._movie_id_and_vector_pairs = movie_id_and_vector_pairs
        self._kp_ids = [d['movie_id'] for d in movie_id_and_vector_pairs]
        self._vectors = [d['vector'] for d in movie_id_and_vector_pairs]

        self._index = nmslib.init(method='sw-graph', space='cosinesimil')
        self._index.addDataPointBatch(self._vectors)
        self._index.createIndex({}, print_progress=True)

    def get_knn_raw(self, query_vector: [float], k=100):
        """
        K nearest neighbours using cosine metrics
        :param query_vector: float vector of user query
        :param k: limit of k nearest neighbours
        :return: list of movie_id of k nearest neighbours using cosine metrics and distances
        """
        ids, distances = self._index.knnQuery(query_vector, k=k)
        real_ids = [self._movie_id_and_vector_pairs[i]['movie_id'] for i in ids]
        return real_ids, distances

    def get_knn(self, query_vector, k=1000):
        """
        K nearest neighbours using cosine metrics
        :param query_vector: float vector of user query
        :param k: limit of k nearest neighbours
        :return: list of UNIQUE movie_id of k nearest neighbours using cosine metrics
        """
        ids, distances = self._index.knnQuery(query_vector, k=10000)
        id_score = {}
        n = len(ids)
        for i in range(n):
            if i < 10:
                cur_score = 1
            else:
                cur_score = 1.0 / (i - 9)
            index = self._kp_ids[ids[i]]
            if index not in id_score:
                id_score[index] = 0
            id_score[index] += cur_score

        items = id_score.items()
        sort_items = sorted(items, key=lambda x: -x[1])  # reversed
        k = min(k, len(sort_items))
        result = [item[0] for item in sort_items]
        return result[:k]
        # result = []
        # count_by_id = {}
        # sum_by_id = {}
        # for i in range(len(ids)):
        #     # if distances[i] > 0.40:
        #     #     break
        #     movie_id = self._movie_id_and_vector_pairs[ids[i]]['movie_id']
        #     if movie_id not in count_by_id:
        #         count_by_id[movie_id] = 0
        #         sum_by_id[movie_id] = 0
        #     count_by_id[movie_id] = count_by_id[movie_id] + 1
        #     sum_by_id[movie_id] = sum_by_id[movie_id] + (k - i)
        #
        # result_sum_by_id = sum_by_id
        #
        # id_with_score = sorted(result_sum_by_id.items(), key=lambda kv: kv[1], reverse=True)

        # result = [item[0] for item in id_with_score]
        # result = [self._movie_id_and_vector_pairs[i]['movie_id']for i in ids]
        #
        # print(result)
        # return result

    def get(self, vector, k):
        ids, distances = self._index.knnQuery(vector, k=k)
        v = [self._vectors[i] for i in ids]
        return v, distances