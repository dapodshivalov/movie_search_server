import pandas as pd
import nmslib
import numpy
# from count import count
import count


class SearchEngine:
    def __init__(self, src):
        count.Count.count_var += 1
        self._vectorized_reviews = pd.read_pickle(src)
        print(self._vectorized_reviews.head())
        print(self._vectorized_reviews.shape[0])
        self._id_to_vector = []
        self._id_to_title = dict()

        for i in range(self._vectorized_reviews.shape[0]):
            self._id_to_vector.append(self._vectorized_reviews.iloc[i]['vector'])
            self._id_to_title[i] = self._vectorized_reviews.iloc[i]['movie_title']

        self._index = nmslib.init(method='sw-graph', space='cosinesimil')
        self._index.addDataPointBatch(self._id_to_vector)
        self._index.createIndex({}, print_progress=True)

    def get_knn_raw(self, query_vector, k=100):
        ids, distances = self._index.knnQuery(query_vector, k=k)
        titles = [self._id_to_title[i] for i in ids]
        return titles, distances

    def get_knn(self, query_vector, k=100):
        ids, distances = self._index.knnQuery(query_vector, k=k)
        result = []
        count_by_title = {}
        sum_by_title = {}
        for i in range(len(ids)):
            title = self._id_to_title[ids[i]]
            if not (title in count_by_title):
                count_by_title[title] = 0
                sum_by_title[title] = 0
            count_by_title[title] = count_by_title[title] + 1
            sum_by_title[title] = sum_by_title[title] + (k - i)

        result_sum_by_title = {}

        for key, value in count_by_title.items():
            if value >= 2:
                result_sum_by_title[key] = sum_by_title[key]

        title_with_score = sorted(result_sum_by_title.items(), key=lambda kv: kv[1], reverse=True)

        result = [item[0] for item in title_with_score]

        print(result)
        return result
