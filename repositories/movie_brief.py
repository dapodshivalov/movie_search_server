class MovieBriefDto:
    def __init__(self, kp_id, title, poster_url, year, rating, genres):
        self.kp_id = int(kp_id)
        self.title = title
        self.poster_url = poster_url
        self.year = year
        self.rating = rating
        self.genres = genres

    def to_dict(self):
        return {
            'kp_id': str(self.kp_id),
            'title': self.title,
            'poster_url': self.poster_url,
            'year': self.year,
            'rating': str(self.rating),
            'genres': self.genres
        }

    class Deserializer:
        def from_dict(self, dict):
            return MovieBriefDto(
                dict['kp_id'],
                dict['title'],
                dict['poster_url'],
                dict['year'],
                dict['rating'],
                dict['genres']
            )