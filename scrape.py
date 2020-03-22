import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import time

from time import sleep
from random import randint

then = time.time()

reviews = []
headings = []
stars = []
dates = []

pages = np.arange(1, 287, 1)

for page in pages:
    page = requests.get("https://uk.trustpilot.com/review/togetherenergy.co.uk" + "?page=" + str(page))

    soup = BeautifulSoup(page.text, "html.parser")
    review_div = soup.find_all('div', class_="review-content")

    sleep(randint(2,10))

    #loop to iterate through reviews
    for container in review_div:

        #Get the body of the review
        nv = container.find_all('p', attrs={'class': 'review-content__text'})
        review = container.p.text if len(nv) == True else '-'
        reviews.append(review)

        #Get the title of the review
        nv1 = container.find_all('h2', attrs={'class': 'review-content__title'})
        heading = container.a.text if len(nv1) == True else '-'
        headings.append(heading)

        #Get the star rating review given
        star = container.find("div", {"class":"star-rating star-rating--medium"}).find('img').get('alt')
        stars.append(star)

        #Get the date
        date_json = json.loads(container.find('script').text)
        date = date_json['publishedDate']
        dates.append(date)



TrustPilot = pd.DataFrame({'Title': headings, 'Body': reviews, 'Rating': stars, 'Date': dates})
TrustPilot['Body'] = TrustPilot['Body'].str.strip()
TrustPilot.to_csv('TrustPilot.csv', index = False)

data = pd.read_csv('TrustPilot.csv')
new = data["Date"].str.split("T", n = 1, expand = True)
data["Date Posted"]= new[0]
data["Time Posted"]= new[1]
data.drop(columns =["Date"], inplace = True)
new = data["Rating"].str.split(":", n = 1, expand = True)
data["Stars"]= new[0]
data["Rated"]= new[1]
data.drop(columns =["Rating"], inplace = True)
data['Time Posted'] = data['Time Posted'].map(lambda x: str(x)[:-4])
data['Stars'] = data['Stars'].map(lambda x: str(x)[0:1])
data = data[['Title', 'Body', 'Stars', 'Rated', 'Date Posted', 'Time Posted']]
data.to_csv('TrustPilot.csv', index = False)

now = time.time()
print("It took: ", now-then, "seconds")
mins = now-then
minute = 60
totalMins = mins / minute
totalMinsRound = round(totalMins, 2)
print("It took: ", totalMinsRound, "minutes and seconds")
