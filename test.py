import requests

url = "https://api.themoviedb.org/3/search/movie?query=Joker&include_adult=false&language=en-US&page=1"



headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMmFjOGY3MjgwOTcwZmFhZjAwZjJkNTZjNzFiZWNmMSIsInN1YiI6IjY1NWE0NjhjNjdkY2M5MDExZGU1YjI0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.BcmPVBlQlEGXL8jYB0ySo8Yy4qUJfdMNgpdBKympEic"
}

response = requests.get(url, headers=headers)

data = response.json()
movie=data['results'][0]
print(movie)
print(movie.id)