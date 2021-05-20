# import pandas as pd
# import requests as rq
# from tqdm import tqdm
# import redis
# import json
# import numpy as np
#
# # api_path = 'https://api.themoviedb.org/3/search/movie'
# api_path = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/'
# poster_prefix = 'https://www.themoviedb.org/t/p/w1280'
#
# def np_encoder(object):
#     if isinstance(object, np.generic):
#         return object.item()
#
# class SerializableToDict:
#     def to_dict(self): raise NotImplementedError()
#
#
# class DeserializerFromDict:
#     def from_dict(self, dict): raise  NotImplementedError()
#
#
# class MovieBrief(SerializableToDict):
#     def __init__(self, kp_id, title, poster_url, release_year, rating, genres):
#         self.kp_id = int(kp_id)
#         self.title = title
#         self.poster_url = poster_url
#         self.release_year = release_year
#         self.rating = rating
#         self.genres = genres
#
#     def to_dict(self):
#         return {
#             'kp_id': str(self.kp_id),
#             'title': self.title,
#             'poster_url': self.poster_url,
#             'release_year': self.release_year,
#             'rating': str(self.rating),
#             'genres': self.genres
#         }
#
#     class Deserializer(DeserializerFromDict):
#         def from_dict(self, dict):
#             return MovieBrief(
#                 dict['kp_id'],
#                 dict['title'],
#                 dict['poster_url'],
#                 dict['release_year'],
#                 dict['rating'],
#                 dict['genres']
#             )
#
#
# # class MovieFull(SerializableToDict):
# #
# #     def __init__(self, kp_id, title, poster_url, release_year, rating, genres):
# #         self.kp_id = int(kp_id)
# #         self.title = title
# #         self.poster_url = poster_url
# #         self.release_year = release_year
# #         self.rating = rating
# #         self.genres = genres
# #
# #     def to_dict(self):
# #         return {
# #             'kp_id': self.kp_id,
# #             'title': self.title,
# #             'poster_url': self.poster_url,
# #             'release_year': self.release_year,
# #             'rating': self.rating,
# #             'genres': self.genres
# #         }
#
# def get_data(id):
#     m = MovieBrief(0, "", poster_prefix + '/7xooTUBDxB8Z2kFuLoIzxaa0NxT.jpg', '1990-11-1', 1, [28])
#
#     response = rq.get(api_path + str(int(id)), params={
#
#         'append_to_response': 'RATING'
#     }, headers={
#         'X-API-KEY': '3ba5f8cf-eb17-4290-901b-82595735d4ef'
#     })
#
#     try:
#         j = response.json()
#         json = j['data']
#         rating = j['rating']
#     except IndexError:
#         print(id)
#         return m
#
#     try:
#         m = MovieBrief(id, json['nameRu'], json['posterUrl'], json['year'], rating['rating'], [d['genre'] for d in json['genres']])
#     except:
#         print("cant construct ", id)
#         return m
#     return m
#
# # def get_full_info(id):
#
# def save_to_redis(client: redis.Redis, entity_name: str, identifier: str, data: dict):
#     json_data = json.dumps(data, default=np_encoder, ensure_ascii=False)
#     key = entity_name + ':' + identifier
#     client.set(key, json_data)
#
# def get_from_redis(client: redis.Redis, entity_name: str, identifier: str):
#     key = entity_name + ':' + identifier
#     value = client.get(key).decode('UTF-8')
#     return json.loads(value)
#
# def
#
# if __name__ == '__main__':
#     # movies = pd.read_csv('data/movie_ids.csv', sep=';')
#     # print(movies.head())
#     # print(get_data(movies.iloc[0]['id']).to_dict())
#     # movie_infos = []
#     # for i in tqdm(range(250)):
#     #     movie_infos.append(get_data(movies.iloc[i]['id']).to_dict())
#     # movies_df = pd.DataFrame(movie_infos, columns=['kp_id', 'title', 'poster_url', 'release_year', 'rating', 'genres'])
#     # movies_df.to_pickle("data/movie_briefs.p")
#
#     # movies_df = pd.read_pickle('data/movie_briefs.p')
#     # titles = ["Начало", "Леон", "Крестный отец", "Криминальное чтиво"]
#     # print(movies_df.head())
#     # # infos = movies_df[movies_df['title'].isin(titles)]
#     # print(movies_df[movies_df['title'].titles])
#
#     client = redis.Redis(host='127.0.0.1')
#
#     # print(client.hgetall('obj1'))
#
#     movies_df = pd.read_pickle('data/movie_briefs.p')
#     print(movies_df.shape)
#     print(movies_df.head())
#     rows_count = movies_df.shape[0]
#     entity_name = 'movie_brief'
#     for i in range(rows_count):
#         value = movies_df.iloc[i].to_dict()
#         identifier = str(value['kp_id'])
#         save_to_redis(client, entity_name, identifier, value)
#
#     # print(type(movies_df.iloc[0].to_dict()['kp_id']))
#     # d = movies_df.iloc[0].to_dict()
#     # print(d)
#     # js_d = json.dumps(d, default=np_encoder, ensure_ascii=False)
#     # print(js_d)
#     # d_loads = json.loads(js_d)
#     # m = MovieBrief.Deserializer().from_dict(d_loads)
#     # print(m.to_dict())
#     # m = MovieBrief.Deserializer().from_dict(m.to_dict())
#     # print(m.to_dict())
#
#     # rows = movies_df[:movies_df.shape[1]]
#     # print(rows[0:5])
#     # sample = [el.to_dict() for el in rows[:5]]
#     # print(sample)