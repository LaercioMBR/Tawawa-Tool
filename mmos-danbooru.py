from numpy import diff
import requests
import json
import unicodedata
from pytwitter import Api
from requests.models import LocationParseError

from bs4 import BeautifulSoup
from requests import get

import time
import re

mmo_json = {
    "meta" :  {
        "MMO Number" : "number",
        "Twitter Source" : "string",
        "Twitter Upload Timestamp" : "date",
        "Danbooru Source" : "string",
        "Character Count" : "number",
        "Character List" : "string",
        "Commentary Title" : "string",
        "Commentary Description" : "string",
        "Translated Commentary Title" : "string",
        "Translated Commentary Description" : "string",
        "Notes" : "string", 
        "Rating" : "string",
        "Number of General Content Tags" : "number",
        "General Content Tags" : "string",
        "Preview file url" : "string", #Danbooru or Twitter, whichever is free to use lol
        "Extra Comment" : "string", #From fandom initially, but it isn't complete and will require revision and new input for the ~150 MMOs that are empty.
    },
    "data" : {
    }
}

rating_dict = {
    "s" : "Safe",
    "q" : "Questionable",
    "e" : "Explicit"
}

fan_descriptions = {}


def populate_json(post_ids):

    #LOOPING THROUGH THE POST_IDS

    data = {}

    for post_id in post_ids:

        post_json = request_post(post_id)
        post_commentary_json = request_commentary(post_id)

        #print("Post json")
        #print(post_json)
        #print("Post commentary json")
        #print(post_commentary_json)

        mmo_number = 0

        if int(post_id) == 1935176:
            mmo_number = "1"
        elif int(post_id) == 2005520:
            mmo_number = "GW SP"
        elif int(post_id) == 2255030:
            mmo_number = "42.5"
        elif int(post_id) == 3683304:
            mmo_number = "247.5"
        elif int(post_id) == 3881766:
            mmo_number = "270.5"
        elif int(post_id) == 3925405:
            mmo_number = "275.5"
        elif int(post_id) == 4193497:
            mmo_number = "299.5"
        elif int(post_id) == 4361483:
            mmo_number = "313.5"
        elif int(post_id) == 4402872:
            mmo_number = "316.5"
        elif int(post_id) == 4528587:
            mmo_number = "326.5"
        
        
        
            
        else:
            mmo_number = discover_mmo_number(post_commentary_json)

        print("MMO NUmber -> ")
        print(mmo_number)
        print("Length of mmo number -> " + str(len(mmo_number)) + "| Type of mmo_number -> " + str(type(mmo_number) ))
        mmo_upload_timestamp = discover_upload_timestamp(post_json["source"])

        temp = str(mmo_number)
        #input("Pause MMO NUMBER 1")
        print(mmo_number)

        try:
            print("Print fan descriptions found" + fan_descriptions[temp])
            #input("Pause MMO NUMBER 2")
            mmo_extra_comment = fan_descriptions[temp]
        except KeyError:
            print("No Fan descriptions for the MMO : " + mmo_number)
            mmo_extra_comment = ""
        finally:

            mmo = {
                "twitter_source" : post_json["source"],
                "mmo_number" : mmo_number,
                "twitter_source_timestamp" : mmo_upload_timestamp,
                "danbooru_source" : "https://danbooru.donmai.us/posts/" + str(post_id),
                "character_count" : post_json["tag_count_character"],
                "character_list" : post_json["tag_string_character"],       
                "commentary_title" : post_commentary_json["original_title"],
                "commentary_description" : post_commentary_json["original_description"],
                "commentary_title_tl" : post_commentary_json["translated_title"],
                "commentary_description_tl" : post_commentary_json["translated_description"],
        #       "notes" : post_notes_json[""],
                "rating" : rating_dict[str(post_json["rating"])],
                "general_tag_count" : post_json["tag_count_general"],
                "general_tag_list" : post_json["tag_string_general"],
                "preview_file_url" : post_json["preview_file_url"],
                "extra_comment" : mmo_extra_comment
            }


        #   print(mmo)

            data[mmo_number] = mmo

            k  = list(data.items())
            print(k[-1])

        #   input("For loop paused, press enter to continue")

def discover_mmo_number(post_commentary_json):

    title = post_commentary_json["original_title"]
    description = post_commentary_json["original_description"]

    title = unicodedata.normalize('NFKC',title)

    print("Title -> " + title)
    numbers_title = []
    count = 0
    temp = []

    for character in title:
        if  ( character.isdigit() or (count >= 1 and (character == "." or character == "," or character.isspace() ) ) ):
            temp.append(character)
            count+=1
        elif count >= 1:
            count = 0
            s = ''.join(temp)
            s.strip()
            temp = []
            numbers_title.append(s)

        #print(character)

    if count >= 1:
        count = 0
        s = ''.join(temp)
        s.strip()
        temp = []
        numbers_title.append(s)
    
    
    selector = -1
    if(len(numbers_title) == 0) or (len(numbers_title) > 1) :
        numbers_title.append("Something fucked up in the number")
        print("Numbers found in the title -> " + str(numbers_title))
        print("Length of the list of numbers in the title -> " + str(len(numbers_title)))

        while int(selector) < 0 or int(selector) >= len(numbers_title):
            print("Numbers found in the title -> " + str(numbers_title))
            selector =  input("There's multiple numbers in the title, please choose which one should be the mmo number(index starts at 0)")
            if (int(selector) > len(numbers_title) ) or (int(selector) < 0 ) or selector is None :
                print("Number chosen is out of bounds")
            elif selector.strip() == "REDO":
                mmo_number = input("Input the MMO number now:")
                return mmo_number



    print("Numbers found")
    print(numbers_title)
    mmo_number = numbers_title[int(selector)]

    mmo_number = unicodedata.normalize('NFKC', mmo_number)
    
    mmo_number = mmo_number.strip()
    print("MMO_Number" +  str(mmo_number))
    return mmo_number

def discover_upload_timestamp(twitter_source):

    if( twitter_source.find("photo") >= 0):
        print("Twitter source has photo on the URL! Twitter source -> " + twitter_source)
        temp =  twitter_source.lower().split("https://twitter.com/strangestone/status/")
        print("Temp before spliting the tweet id" + str(temp))
        tweet_id =   temp[1].lower().split("/photo/1")
    else:
        tweet_id =   twitter_source.lower().split("https://twitter.com/strangestone/status/")    

    print("Tweet id list " + str(tweet_id))

    for i in tweet_id:
        if len(i) != 0:
            id = i

    print("Final tweet ID ->" + id)

    twitter_api_url = "https://api.twitter.com/2/tweets?ids="
    twitter_request = twitter_api_url + str(id)
    

    token_file = open("token.env","r",encoding="utf-8")
    token = token_file.read()
    bearer_token = "Bearer " + str(token)

    params = {"tweet.fields" : "created_at"}
    header = {'Authorization': bearer_token}

    try:

        resp_twitter = requests.get(url=twitter_request, params=params, headers=header)
        twitter_json = resp_twitter.json()
        
        print("Twitter json ->")
        print(twitter_json)
        #print(twitter_json)
        
    #    print(link)

        timestamp = twitter_json["data"][0]["created_at"]
    except KeyError:
        temp_id = input("Something went wrong while getting the Twitter Timestamp, please input the correct id now:")
        twitter_request = twitter_api_url + str(temp_id).strip()

        resp_twitter = requests.get(url=twitter_request, params=params, headers=header)
        twitter_json = resp_twitter.json()
        
        print("Twitter json ->")
        print(twitter_json)
        #print(twitter_json)
        
    #    print(link)
        timestamp = twitter_json["data"][0]["created_at"]

    #    timestamp = link.time.datetime
        #print(timestamp)
        #input("Inside discover upload timestamp")
    finally:
        return timestamp

def fan_extra_comment():

    #input("Inside discover extra comment")

    url = "https://tawawa.fandom.com/wiki/List_of_Illustrations"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    tables = soup.find_all("table", class_="article-table") 

    print

    mmo_number = 0
    fan_description = ""
    for table in tables:
        for tbody in table:
            for tr in tbody:
#                print("Table row " + str(tr))
#                input("Pause table row")
                if str(tr).find("</th") > 0 :
                    continue
                for idx,td in enumerate(tr):                    
#                    print("idx -> " + str(idx))
#                    print("td -> " + str(td))
#                    input("Pause td")
                    if idx == 1:
                        mmo_number = str(td.text).strip()
                    if idx == 7:
                        fan_description = td.text.strip()
#                print("MMO_number in fandom -> " + str(mmo_number))
#                print("Fan description in fandom ->" + str(fan_description))
#                input("Pause table row 2")
                fan_descriptions[mmo_number] = fan_description
#                print(fan_descriptions)
        
#        input("Pause table")
    
    print(fan_descriptions)

def request_pool(pool_id):
    url_pools_api = 'https://danbooru.donmai.us/pools/'
    url_http_request = url_pools_api + str(pool_id) + '.json'

    params = dict()

    resp_pool = requests.get(url=url_http_request, params=params)
    pool_json = resp_pool.json()

    return pool_json

def request_post(post_id):
    url_posts_api = 'https://danbooru.donmai.us/posts/'
    url_http_request = url_posts_api + str(post_id) + '.json'

    params = dict()

    resp_post = requests.get(url=url_http_request, params=params)
    post_json = resp_post.json()

    return post_json

def request_commentary(post_id):
    url_post_commentary_api = 'https://danbooru.donmai.us/posts/'
    url_http_request = url_post_commentary_api + str(post_id) + '/artist_commentary.json'
    
    params = dict()

    resp_post = requests.get(url=url_http_request, params=params)
    post_commentary_json = resp_post.json()

    return post_commentary_json

def main():

    pool_id = 10374

    pool_json = request_pool(pool_id)
    
    post_ids = pool_json["post_ids"]

    fan_extra_comment()

    populate_json(post_ids)

    with open('mmo.json', 'w') as outfile:
        json.dump(mmo_json, outfile)

if __name__ == "__main__":
    main()