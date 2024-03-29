from numpy import diff, number
import requests
import json
import unicodedata
from pytwitter import Api
from requests.models import LocationParseError

from bs4 import BeautifulSoup
from requests import get

import time
import re
import os

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
        "Number of Copyright Tags" : "number",
        "Copyright Tags" : "string",
        "Preview file url" : "string", #Danbooru or Twitter, whichever is free to use lol
        "Extra Comment" : "string", #From fandom initially, but it isn't complete and will require revision and new input for the ~150 MMOs that are empty.
    },
    "data" : [

    ],
    "unique_character_list" : [

    ],
    "unique_copyright_list" : [

    ],
    "unique_tag_list" : [

    ]

}

rating_dict = {
    "s" : "Safe",
    "q" : "Questionable",
    "e" : "Explicit"
}

fan_descriptions = {}

def populate_mmo_json(post_ids):

    #LOOPING THROUGH THE POST_IDS

    data = {}
    twitter_posts_id = {}

    for post_id in post_ids:

        post_json = request_post(post_id)

        post_commentary_json = request_commentary(post_id)

        mmo_number = discover_mmo_number(post_id, post_commentary_json)        
        
        mmo = populate_mmo_info(mmo_number, post_json, post_commentary_json)

        mmo = populate_unique_character_json(mmo , post_json)

        mmo = populate_unique_copyright_json(mmo , post_json)

        mmo = populate_unique_tag_json(mmo , post_json)

        twitter_posts_id[mmo_number] = post_json["source"]

        data[mmo_number] = mmo
    
    
    data = populate_timestamp_info_mmo(data, twitter_posts_id)
    
    return data

def populate_timestamp_info_mmo(data , twitter_posts_id):
    timestamps = discover_upload_timestamp(twitter_posts_id)
    
    print(timestamps)
    print("Timestamps above")
#    input("Pause timestamps")
    temp = 0
    for key, mmo in data.items():
        timestamp = timestamps[temp]
        mmo["twitter_source_timestamp"] = timestamp
        temp = temp + 1

        data[key] = mmo

        print(data[key])
        #input()
    return data

def populate_mmo_info(mmo_number , post_json, post_commentary_json):

    post_id = post_json["id"]
#       print("Danbooru Post ID -> " + str(post_id))
        #print("Post json")
        #print(post_json)
        #print("Post commentary json")
        #print(post_commentary_json)
#        print("MMO NUmber -> ")
#        print(mmo_number)
#        print("Length of mmo number -> " + str(len(mmo_number)) + "| Type of mmo_number -> " + str(type(mmo_number) ))

        #input("Pause MMO NUMBER 1")
        #print(mmo_number)

    check = 0

#    print(mmo_number)
#    print(post_json)
#    print(post_commentary_json)
#    input()
    print(mmo_number)
    mmo_extra_comment = ""
    try:
        #print("Print fan descriptions found" + fan_descriptions[temp])
        #input("Pause MMO NUMBER 2")
        mmo_extra_comment = fan_descriptions[mmo_number]
            
    except KeyError as e:
        print(e)
        if e.args[0] == None:
            #print("No Fan descriptions for the MMO : " + mmo_number)
            mmo_extra_comment = ""
    finally:

        try:
            mmo_commentary_title = post_commentary_json["original_title"]
        except KeyError as e:
            if e.args[0] == 'original_title':
                check = 1
                mmo_commentary_title = ""
                mmo_commentary_description = ""
                mmo_commentary_title_tl = ""
                mmo_commentary_description_tl = ""
        finally:
                
            if check == 0:
                mmo_commentary_title = post_commentary_json["original_title"]
                mmo_commentary_description = post_commentary_json["original_description"]
                mmo_commentary_title_tl = post_commentary_json["translated_title"]
                mmo_commentary_description_tl = post_commentary_json["translated_description"]

            mmo_character_string = post_json["tag_string_character"]
            mmo_character_count = post_json["tag_count_character"]


            mmo = {
                "twitter_source" : post_json["source"],
                "mmo_number" : mmo_number,
                "twitter_source_timestamp" : '',                    
                "danbooru_source" : "https://danbooru.donmai.us/posts/" + str(post_id),
                "character_count" : mmo_character_count,
                "character_list" : mmo_character_string,       
                "commentary_title" : mmo_commentary_title,
                "commentary_description" : mmo_commentary_description,
                "commentary_title_tl" : mmo_commentary_title_tl,
                "commentary_description_tl" : mmo_commentary_description_tl,
        #       "notes" : post_notes_json[""],
                "rating" : rating_dict[str(post_json["rating"])],
                "general_tag_count" : post_json["tag_count_general"],
                "general_tag_list" : post_json["tag_string_general"],
                "copyright_list" : post_json["tag_string_copyright"],
                "copyright_list_count" : post_json["tag_count_copyright"],
                "preview_file_url" : post_json["preview_file_url"],
                "extra_comment" : mmo_extra_comment
            }

            #   print(mmo)

            return mmo

            #k  = list(data.items())
            #print(k[-1])

            #   input("For loop paused, press enter to continue")


def populate_unique_character_json(mmo, post_json):

    mmo_character_string = mmo["character_list"]

    mmo_character_list = mmo_character_string.split(" ")

#    print("MMO character list")
#    print(mmo_character_list)
    
    dict_prevent_infinite = {}
    dict_all_characters = {}

    for character in mmo_json["unique_character_list"]:
        dict_all_characters[character["character_name"]] = 1

    for character in mmo_character_list :

#        print("character")
#        print(character)
        

        # Check if the final list is empty, if it is, add the first character to the list if it exists
        if len(mmo_json["unique_character_list"]) == 0 and len(character) > 0 :
            unique_character = { 
                "character_name" : character , 
                "mmo_appearance_count" : 1,
                "mmo_number_appearances" : [mmo["mmo_number"]]
            }

            mmo_json["unique_character_list"].append(unique_character)

            dict_prevent_infinite[character] = 1
        elif character:
            count = 0


            for character_json in mmo_json["unique_character_list"]:
#                print("CHaracter json")
#                print(character_json)
#                print("count  " + str(count))
#                print("mmo nmumber :  " + str(mmo["mmo_number"]))

                if character not in dict_prevent_infinite: 

                    if character == character_json["character_name"]: 

                        mmo_json["unique_character_list"][count]["mmo_appearance_count"] += 1
                        
                        mmo_json["unique_character_list"][count]["mmo_number_appearances"].append(mmo["mmo_number"])

                        dict_prevent_infinite[character] = 1
                    elif character not in dict_all_characters:

                        unique_character = { 
                            "character_name" : character , 
                            "mmo_appearance_count" : 1,
                            "mmo_number_appearances" : [mmo["mmo_number"]]
                        }

                        mmo_json["unique_character_list"].append(unique_character)

                        dict_prevent_infinite[character] = 1
                    
                count += 1

#    print("mmo_json_unique_character_list")
#    print(mmo_json["unique_character_list"])
#    input()
    return mmo

def populate_unique_copyright_json(mmo, post_json):

    mmo_copyright_string = post_json["tag_string_copyright"]

    mmo_copyright_list = mmo_copyright_string.split(" ")

#    print("MMO character list")
#    print(mmo_character_list)
    
    dict_prevent_infinite = {}
    dict_all_copyright = {}

    for copyright in mmo_json["unique_copyright_list"]:
        dict_all_copyright[copyright["copyright_name"]] = 1

    for copyright in mmo_copyright_list :

#        print("character")
#        print(character)
        

        # Check if the final list is empty, if it is, add the first character to the list if it exists
        if len(mmo_json["unique_copyright_list"]) == 0 and len(copyright) > 0 :
            unique_copyright = { 
                "copyright_name" : copyright , 
                "mmo_appearance_count" : 1,
                "mmo_number_appearances" : [mmo["mmo_number"]]
            }

            mmo_json["unique_copyright_list"].append(unique_copyright)

            dict_prevent_infinite[copyright] = 1
        elif copyright:
            count = 0

            for copyright_json in mmo_json["unique_copyright_list"]:
#                print("CHaracter json")
#                print(character_json)
#                print("count  " + str(count))
                #print("mmo nmumber :  " + str(mmo["mmo_number"]))

                if copyright not in dict_prevent_infinite: 

                    if copyright == copyright_json["copyright_name"]: 

                        mmo_json["unique_copyright_list"][count]["mmo_appearance_count"] += 1
                        
                        mmo_json["unique_copyright_list"][count]["mmo_number_appearances"].append(mmo["mmo_number"])

                        dict_prevent_infinite[copyright] = 1
                    elif copyright not in dict_all_copyright:

                        unique_copyright = { 
                            "copyright_name" : copyright , 
                            "mmo_appearance_count" : 1,
                            "mmo_number_appearances" : [mmo["mmo_number"]]
                        }

                        mmo_json["unique_copyright_list"].append(unique_copyright)

                        dict_prevent_infinite[copyright] = 1
                    
                count += 1

#    print("mmo_json_unique_character_list")
#    print(mmo_json["unique_character_list"])
#    input()
    return mmo

def populate_unique_tag_json(mmo, post_json):

    mmo_tag_string = post_json["tag_string_general"]

    mmo_tag_list = mmo_tag_string.split(" ")

#    print("MMO character list")
#    print(mmo_character_list)
    
    dict_prevent_infinite = {}
    dict_all_tag = {}

    for tag in mmo_json["unique_tag_list"]:
        dict_all_tag[tag["tag_name"]] = 1

    for tag in mmo_tag_list :

#        print("character")
#        print(character)
        

        # Check if the final list is empty, if it is, add the first character to the list if it exists
        if len(mmo_json["unique_tag_list"]) == 0 and len(tag) > 0 :
            unique_tag = { 
                "tag_name" : tag , 
                "mmo_appearance_count" : 1,
                "mmo_number_appearances" : [mmo["mmo_number"]]
            }

            mmo_json["unique_tag_list"].append(unique_tag)

            dict_prevent_infinite[tag] = 1
        elif tag:
            count = 0

            for tag_json in mmo_json["unique_tag_list"]:
#                print("CHaracter json")
#                print(character_json)
#                print("count  " + str(count))
                #print("mmo nmumber :  " + str(mmo["mmo_number"]))

                if tag not in dict_prevent_infinite: 

                    if tag == tag_json["tag_name"]: 

                        mmo_json["unique_tag_list"][count]["mmo_appearance_count"] += 1
                        
                        mmo_json["unique_tag_list"][count]["mmo_number_appearances"].append(mmo["mmo_number"])

                        dict_prevent_infinite[tag] = 1
                    elif tag not in dict_all_tag:

                        unique_tag = { 
                            "tag_name" : tag , 
                            "mmo_appearance_count" : 1,
                            "mmo_number_appearances" : [mmo["mmo_number"]]
                        }

                        mmo_json["unique_tag_list"].append(unique_tag)

                        dict_prevent_infinite[tag] = 1
                    
                count += 1

#    print("mmo_json_unique_character_list")
#    print(mmo_json["unique_character_list"])
#    input()
    return mmo


def discover_mmo_number(post_id , post_commentary_json):

    try:
        post_id = post_commentary_json["post_id"]
    except KeyError as e:
        print("Error because no artist commentary on the post")
        post_id = post_id

    finally:

        mmo_number = 0

        if int(post_id) == 1935176:
            mmo_number = "1"
        elif int(post_id) == 2005520:
            mmo_number = "GW SP"
        elif int(post_id) == 2187905:
            mmo_number = "40"
        elif int(post_id) == 2195135:
            mmo_number = "41"            
        elif int(post_id) == 2255030:
            mmo_number = "42.5"
        elif int(post_id) == 2302813:
            mmo_number = "56"
        elif int(post_id) == 2899696:
            mmo_number = "140"
        elif int(post_id) == 3643258:
            mmo_number = "241"
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
        elif int(post_id) == 4474821:
            mmo_number = "322"
        elif int(post_id) == 4528587:
            mmo_number = "326.5"
        elif int(post_id) == 4647416:
            mmo_number = "335"
        elif int(post_id) == 4866673:
            mmo_number = "349"
        
        elif mmo_number == 0:

            title = post_commentary_json["original_title"]
            description = post_commentary_json["original_description"]

            title = unicodedata.normalize('NFKC',title)

            #print("Title -> " + title)
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
                    if selector.strip() == "100" :
                        mmo_number = input("Input the MMO number now:")
                        return mmo_number
                    elif (int(selector) > len(numbers_title) ) or (int(selector) < 0 ) or selector is None :
                        print("Number chosen is out of bounds")

        #    print("Numbers found")
        #    print(numbers_title)
            mmo_number = numbers_title[int(selector)]

            mmo_number = unicodedata.normalize('NFKC', mmo_number)
            
            mmo_number = mmo_number.strip()
        #    print("MMO_Number" +  str(mmo_number))
        
        return mmo_number

def discover_upload_timestamp(twitter_source_list):

    print(twitter_source_list)
#    input("Twitter sources list above")
    twitter_timestamps_json = []
    id_list = []
    count = 0
    total = 1
    for key, value in twitter_source_list.items():
        
        if( value.find("photo") >= 0):
            print("Twitter source has photo on the URL! Twitter source value -> " + str(value))
            temp =  value.lower().split("https://twitter.com/strangestone/status/")
            print("Temp before spliting the tweet id" + str(temp))
            tweet_id =   temp[1].lower().split("/photo/1")
        else:
            tweet_id =   value.lower().split("https://twitter.com/strangestone/status/")    

        print("Tweet id list " + str(tweet_id))

        for i in tweet_id:
            if len(i) != 0:
                id = i

        print(id)
        id_list.append(id)
        print("Final tweet ID -> {id} ")

        if (((count + 1) % 100 ) == 0) or (total == len(twitter_source_list)):
            count=0
            twitter_api_url = "https://api.twitter.com/2/tweets?ids="

            print(id_list)
            print("Id list above")
#            input("Pause id List")

            string_ids = ""
            for id in id_list:
                string_ids = string_ids + str(id)+ ","

            string_ids = string_ids[:-1]

            print(string_ids)
            print("Id string above")
#            input("Pause id List")

            twitter_request = twitter_api_url + string_ids
            
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
                
            except Exception:
                temp_id = input("Something went wrong while getting the Twitter Timestamp, please input the correct id now:")
                twitter_request = twitter_api_url + str(temp_id).strip()

                resp_twitter = requests.get(url=twitter_request, params=params, headers=header)
                twitter_json = resp_twitter.json()
                
                print("Twitter json ->")
                print(twitter_json)
                
            #    print(link)
                timestamp = twitter_json["data"][0]["created_at"]

            #    timestamp = link.time.datetime
                #print(timestamp)
                #input("Inside discover upload timestamp")
            finally:
                                              
                for item in twitter_json["data"]:
                    print(item)
                    time = item["created_at"]
                    twitter_timestamps_json.append(time)


                id_list = []
        count = count + 1 
        total = total + 1
    return twitter_timestamps_json

def fan_extra_comment():

    #input("Inside discover extra comment")

    url = "https://tawawa.fandom.com/wiki/List_of_Illustrations"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    tables = soup.find_all("table", class_="article-table") 

    #print

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

    data = populate_mmo_json(post_ids)

    mmo_json["data"] = data
    
    with open('mmo.json', 'w') as outfile:
        json.dump(mmo_json, outfile)

if __name__ == "__main__":
    main()