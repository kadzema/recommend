# scrape for user profile
import csv
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def user_scrape(username):
    #  build user url
    url = f"https://www.beeradvocate.com/user/beers/?ba={username}&order=ratingD&start=0&view=R"
    
    #  make request 
    response = requests.get(url)
    
    # beatiful soup object
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # grab user info table
    profile_table = soup.find("div", class_ = "pairsJustified")
    
    # data-points
    dls = profile_table.find_all('dl')
    
    #  dictionary holding user states
    profile_dict = {"user_name" : username}
    
    # loop through table items and make dictionary keys and values
    for dl in dls:
        profile_dict[dl.find('dt').text] = dl.find('dd').text
    
    # get the ratings table on the page
    table = soup.find('table')
    # get the ratings by row
    user_ratings = table.find_all('tr')[3:]
    
    # list for top 3
    top_3 = []

    beer_links = []
    for x in range(3):
        text_info = user_ratings[x].find_all('a')
        num_info = user_ratings[x].find_all('td')[-3:-1]
        base_url_ba = "https://www.beeradvocate.com"
        beer_link = base_url_ba + text_info[0]['href'][0:text_info[0]['href'].find("?")]
        beer_links.append(beer_link)
        top_3_dict = {"Beer Name": text_info[0].text,
                     "Brewery": text_info[1].text,
                     "Beer Style": text_info[2].text,
                     "ABV": num_info[0].text,
                     "User Rating": num_info[1].text}
        top_3.append(top_3_dict)
        
    for link in beer_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        beerimages = soup.find('div', {'id': 'main_pic_norm'}).find_all('img')
        beerlink = beerimages[0]['src']
        if (beerlink is not None):
            top_3_dict['image_link'] = beerlink
        else:
            top_3_dict['image_link'] = ""

    return profile_dict, top_3
    


    


