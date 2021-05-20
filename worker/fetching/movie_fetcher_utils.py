import requests as rq

from repositories.movie_full import MovieFullDto

api_path = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/'


def list_of_dicts_to_list_of_str(dicts, key):
    return [d[key] for d in dicts]


def get_movie_full_info(identifier):
    m = None

    response = rq.get(api_path + str(int(identifier)), params={

        'append_to_response': 'RATING'
    }, headers={
        'X-API-KEY': '3ba5f8cf-eb17-4290-901b-82595735d4ef'
    })

    try:
        js = response.json()
        data = js['data']
        rating = js['rating']['rating']
    except IndexError:
        print(identifier)
        return m

    try:
        m = MovieFullDto(
            data['filmId'],
            data['nameRu'],
            rating,
            data['webUrl'],
            data['posterUrl'],
            data['year'],
            data['filmLength'],
            data['slogan'],
            data['description'],
            data['type'],
            data['ratingMpaa'],
            data['ratingAgeLimits'],
            list_of_dicts_to_list_of_str(data['countries'], 'country'),
            list_of_dicts_to_list_of_str(data['genres'], 'genre')
        )
    except:
        print("cant construct ", identifier)
        return m
    return m



# if __name__ == '__main__':
    # movies = pd.read_csv('data/movie_ids.csv', sep=';')
    # print(movies.head())
    # print(get_data(movies.iloc[0]['id']).to_dict())
    # movie_infos = []
    # for i in tqdm(range(250)):
    #     movie_infos.append(get_data(movies.iloc[i]['id']).to_dict())
    # movies_df = pd.DataFrame(movie_infos, columns=['kp_id', 'title', 'poster_url', 'release_year', 'rating', 'genres'])
    # movies_df.to_pickle("data/movie_briefs.p")

    # movies_df = pd.read_pickle('data/movie_briefs.p')
    # titles = ["Начало", "Леон", "Крестный отец", "Криминальное чтиво"]
    # print(movies_df.head())
    # # infos = movies_df[movies_df['title'].isin(titles)]
    # print(movies_df[movies_df['title'].titles])

    # client = redis.Redis(host='127.0.0.1')

    # print(client.hgetall('obj1'))

    # movies_df = pd.read_pickle('data/movie_briefs.p')
    # print(movies_df.shape)
    # print(movies_df.head())
    # rows_count = movies_df.shape[0]
    # entity_name = 'movie_brief'
    # for i in range(rows_count):
    #     value = movies_df.iloc[i].to_dict()
    #     identifier = str(value['kp_id'])
    #     save_to_redis(client, entity_name, identifier, value)

    # print(type(movies_df.iloc[0].to_dict()['kp_id']))
    # d = movies_df.iloc[0].to_dict()
    # print(d)
    # js_d = json.dumps(d, default=np_encoder, ensure_ascii=False)
    # print(js_d)
    # d_loads = json.loads(js_d)
    # m = MovieBrief.Deserializer().from_dict(d_loads)
    # print(m.to_dict())
    # m = MovieBrief.Deserializer().from_dict(m.to_dict())
    # print(m.to_dict())

    # rows = movies_df[:movies_df.shape[1]]
    # print(rows[0:5])
    # sample = [el.to_dict() for el in rows[:5]]
    # print(sample)