from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

soup = BeautifulSoup(url_get.content,"html.parser")
movie_containers = soup.find_all('div', class_ = 'lister-item mode-advanced') 
# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
votes = []
genres = []
durations = []

# Extract data from individual movie container
for container in movie_containers:
# If the movie has Metascore, then extract:
    if container.find('div') is not None:

        # The name
        name = container.h3.a.text
        names.append(name)

        # The year
        year = container.h3.find('span', class_ = 'lister-item-year').text
        years.append(year)
        
        #duration
        duration = container.p.find('span', class_ = 'runtime').text
        durations.append(duration)
        
        #genres
        genre = container.p.find('span', class_ = 'genre').text
        genres.append(genre)

        # The IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # The number of votes
        vote = container.find('span', attrs = {'name':'nv'})['data-value']
        votes.append(int(vote))

#change into dataframe
df = pd.DataFrame({'movie': names,
'durasi(menit)': durations,
'genre': genres,
'year': years,
'imdb': imdb_ratings,
'votes': votes
})

#insert data wrangling here
df['year'] = df['year'].str.replace(")", "")
df['year'] = df['year'].str.replace("(", "")
df['year'] = df['year'].str.replace("–", "")

df['durasi(menit)'] = df['durasi(menit)'].str.replace(" min", "")

df['genre'] = df['genre'].str.replace("\n", "")

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'imdb {df["votes"].mean().round(2)}'

	# generate plot
	ax = df.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
