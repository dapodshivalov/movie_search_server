# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json

from repositories.film import FilmDto
from repositories.review import ReviewDto


def get_k_reviews(film_id, k) -> [ReviewDto]:
    pages = k // 20 + (1 if k % 20 > 0 else 0)
    review_ids = get_all_review_ids(film_id, until_page=pages)[:k]
    reviews = [get_review(film_id, None, review_id) for review_id in review_ids]
    return reviews


def get_all_reviews(film: FilmDto, until_page=30) -> [ReviewDto]:
    film_id = film.film_id
    review_ids = get_all_review_ids(film_id, until_page=until_page)
    reviews = [get_review(film.film_id, film.title, review_id) for review_id in review_ids]
    return reviews


def get_all_review_ids(film_id, until_page=30) -> [int]:
    reviews = []
    next_page = 1
    total_page = 1
    while next_page <= total_page and next_page <= until_page:
        url = 'https://kinopoiskapiunofficial.tech/api/v1/reviews'
        headers = {'X-API-KEY': '3ba5f8cf-eb17-4290-901b-82595735d4ef'}
        params = {'filmId': film_id, 'page': next_page}
        r = requests.get(url, headers=headers, params=params)
        response_js = json.loads(r.content.decode(encoding='UTF-8'))

        total_page = response_js['pagesCount']
        if total_page is None:
            return []
        next_page += 1
        reviews += [review['reviewId'] for review in response_js['reviews']]
    return reviews


def get_all_review_ids_on_page(film_id, page) -> [ReviewDto]:
    url = 'https://kinopoiskapiunofficial.tech/api/v1/reviews'
    headers = {'X-API-KEY': '3ba5f8cf-eb17-4290-901b-82595735d4ef'}
    params = {'filmId': film_id, 'page': page}
    r = requests.get(url, headers=headers, params=params)
    response_js = json.loads(r.content.decode(encoding='UTF-8'))
    review_ids = [review['reviewId'] for review in response_js['reviews']]
    return review_ids


def get_review(film_id, title, review_id) -> ReviewDto:
    url = 'https://kinopoiskapiunofficial.tech/api/v1/reviews/details'
    headers = {'X-API-KEY': '3ba5f8cf-eb17-4290-901b-82595735d4ef'}
    params = {'reviewId': review_id}
    r = requests.get(url, headers=headers, params=params)
    response_js = json.loads(r.content.decode(encoding='UTF-8'))
    return ReviewDto(film_id, title, review_id, response_js['reviewDescription'])


def get_top() -> [FilmDto]:
    films = []
    next_page = 1
    total_page = 1
    while next_page <= total_page:
        url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/top'
        headers = {'X-API-KEY': '3ba5f8cf-eb17-4290-901b-82595735d4ef'}
        params = {'type': 'TOP_250_BEST_FILMS', 'page': next_page}
        r = requests.get(url, headers=headers, params=params)
        response_js = json.loads(r.content.decode(encoding='UTF-8'))

        total_page = response_js['pagesCount']
        next_page += 1
        films += [FilmDto(film['filmId'], film['nameRu']) for film in response_js['films']]
    return films





# def script_get_top(session: Session):
#     films = get_top()
#     pbar = tqdm(range(len(films)), colour='white')
#     for i in pbar:
#         append_film(session, films[i])
#         pbar.set_description('Saved film: ' + str(films[i].title))



# def script_review_to_csv(reviews: [Review], file_name: str):
#     df = pd.DataFrame(columns=['id', 'movie_title', 'kp_movie_id', 'kp_review_id', 'text', 'status'])
#     for review in reviews:
#         new_row = pd.Series({
#             'id': review.id,
#             'movie_title': review.movie_title,
#             'kp_movie_id': review.kp_movie_id,
#             'kp_review_id': review.kp_review_id,
#             'text': review.text,
#             'status': review.status
#         })
#         df = df.append(new_row, ignore_index=True)
#
#     df.to_excel(file_name)


# def main(name):
#     pass
    # script_get_top(session)
    # script_get_reviews(session)

    # films = get_films_from_queue(session, FilmStatus.PROCESSING, 100)
    # for film in films:
    #     change_film_status(session, film, FilmStatus.RECEIVED)
    #     print(film.title)
    # reviews = get_raw_reviews_from_queue(session, ReviewStatus.RECEIVED, 10000)
    # script_review_to_csv(reviews, "raw_reviews.xlsx")


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
