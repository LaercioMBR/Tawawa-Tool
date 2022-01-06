from numpy import diff
import requests
import json

from requests.models import LocationParseError

#URLs for GET REQUEST
url_posts = 'https://danbooru.donmai.us/posts/'
url_pools = 'https://danbooru.donmai.us/pools/'

#GET REQUEST TAWAWA POOL
url_http = url_pools + str(10374)

url_final = url_http + '.json'

params = dict()

resp_pool = requests.get(url=url_final, params=params)
data_pool = resp_pool.json()

#POST_IDS OF THE POOL
post_ids = data_pool["post_ids"]

print(post_ids)


#OPENING OUTPUT FILE
f = open("Tawawa_output.txt", "w")




mmos_dict = {
    "meta" :  {
        "MMO Number" : "number",
        "Twitter Source" : "string",
        "Twitter Upload Date" : "date",
        "Danbooru Source" : "string",
        "Character Count" : "number",
        "Characters" : "string",
        "Commentary Title" : "string",
        "Commentary Description" : "string",
        "Notes" : "string", 
        "Rating" : "string",
        "Number of General Content Tags" : "number",
        "General Content Tags" : "string",
        "Preview file url" : "string", #Danbooru or Twitter, whichever is free to use lol
        "Extra Comment" : "string",
    },
    "data" : {
        
    }
}

#LOOPING THROUGH THE POST_IDS
for post_id in post_ids:

#GET REQUEST POSTS IN TAWAWA POOL
    url_http = url_posts + str(post_id)
    url_final = url_http + '.json'

#    print(url_final)
#    print(post_id)

    resp_post = requests.get(url=url_final, params=params)
    data_post = resp_post.json() # Check the JSON Response Content documentation below

    print(data_post)

    url_comment = url_http + '/artist_commentary.json'

    resp_comment = requests.get(url=url_comment, params=params)
    data_comment = resp_comment.json() # Check the JSON Response Content documentation below

    print(data_comment)

    input("Press Enter to continue... POST JSON")

    character_count = data_post["tag_count_character"]
    twitter_link = data_post["source"]

    if( character_count > 0):
#        print("Characters present: " + str(character_count ) )
        character_string = data_post["tag_string_character"]
#        print("Characters name : " + character_string )
    else:
#        print("No recurring character present")
        character_string = "No recurring character present"

    f.write (url_http + ";" + twitter_link + ";" + str(character_count) + ";" + character_string + ";" +'\n')

f.close()



f = open("Tawawa_output.txt", "r")

for line in f:
    line_split = line.split(";")

    print(line_split)

    if(int(line_split[2]) > 0):
        print(line_split[3])

f.close()