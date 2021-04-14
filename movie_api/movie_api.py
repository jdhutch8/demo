import colorgram
import urllib.request
import requests
import json
import time
url = 'https://api.themoviedb.org/3/movie/102?api_key=6e2f8f7b92505535bcfddfab21fa170b&language=en-US'
url = 'https://api.themoviedb.org/3/movie/100/images?api_key=6e2f8f7b92505535bcfddfab21fa170b&language=en-US'

with open('api.key', 'r') as key:
    api_key = key.read()

#for i in range(2700, 4000):
#    url = 'https://api.themoviedb.org/3/movie/' + str(i) + '?api_key=6e2f8f7b92505535bcfddfab21fa170b&language=en-US'
#    r = requests.get(url=url)
#    try:
#        title = "movie_details/" + "-".join(r.json()['title'].replace(",", "").replace("/","").replace("?","").split(" ")) + "_" +r.json()['release_date'].split("-")[0] + ".json"
#        print(title)
#        with open(title, "w") as file:
#            json.dump(r.json(), file, indent=4)
#        time.sleep(5)
#    except KeyError:
#        continue
urllib.request.urlretrieve('https://image.tmdb.org/t/p/w500/gghD2ZIPjMzLnnBuT3AZQGYnIW9.jpg', 'posters/ring_test.jpg')



colors = colorgram.extract('posters/ring_test.jpg', 5)
sorted_colors = sorted(colors, key=lambda c: c.proportion)[::-1]

for i in sorted_colors:
    print(i.rgb, i.proportion)
