## SI507 Winter2018
## 009 (Jie-wei Wu)
## Project 1
## Siyu Jia (uniqname: siyujia)


import json
import webbrowser
import requests
import math


############ Part 1 ################
class Media:

    def __init__(self, title = "No Title", author = "No Author", year = "No Year", json = None, url = "No URL"):
        if json is None:
            self.title = title
            self.author = author
            # add another instance variable: release year
            self.release_year = year
            self.preview = url
        else:
            self.author = json['artistName']
            self.release_year = json['releaseDate'][0:4]
            if json['wrapperType'] == "track":
                self.title = json['trackName']
                self.preview = json['trackViewUrl']
            else:
                self.title = json['collectionName']
                self.preview = json['collectionViewUrl']

    # create __str__ method
    def __str__(self):
        return "{} by {} ({})".format(self.title, self.author, self.release_year)

    # create __len__ method and return 0
    def __len__(self):
        return 0


##### create Song, the subclass of Media #####
class Song(Media):

    # add additional instance variables: album, track length
    def __init__(self, title = "No Title", author = "No Author", year= "No Year", album = "No Album", genre = "No Genre", track_len = 0, json = None, url = "No URL"):

        super().__init__(title, author, year,json)
        if json is None:
            self.album = album
            self.track_len = track_len
            self.genre = genre
        else:
            self.album = json['collectionName']
            self.track_len = json['trackTimeMillis']
            self.genre = json['primaryGenreName']

    def __str__(self):
        return super().__str__() + " [{}]".format(self.genre)

    def __len__(self):
        return int(self.track_len / 1000)


##### create Movie, the subclass of Media #####
class Movie(Media):

    #add additional instance variables: rating, movie length
    def __init__(self, title = "No Title", author = "No Author", year = "No Year", rating = "No Rating", movie_len = 0, json = None, url = "No URL"):
        super().__init__(title, author, year, json)
        if json is None:
            self.rating = rating
            self.movie_len = movie_len
        else:
            self.rating = json['contentAdvisoryRating']
            self.movie_len = json['trackTimeMillis']

    def __str__(self):
        return super().__str__() + " [{}]".format(self.rating)

    def __len__(self):
        total_second = int(self.movie_len / 1000)
        minute = int(total_second / 60)
        return minute



################### Part 2 ######################
def create_objects(json_lst):

    song_lst = []
    movie_lst = []
    other_lst = []

    for item in json_lst:
        if "kind" in item:
            if item["kind"] == "song":

                song_lst.append(Song(json = item))
            elif item["kind"] == "feature-movie":
                movie_lst.append(Movie(json = item))
        else:
            other_lst.append(Media(json = item))

    return {"SONGS": song_lst, "MOVIES": movie_lst, "OTHER MEDIA": other_lst}


    # for song in song_lst:
    #     print(inst)
    # for movie in movie_lst:
    #     print(movie)
    # for other in other_lst:
    #     print(other)



############## get and cache iTunes data ###############
CACHE_ITUNES = 'itunes_cache.json'

try:
	cache_file = open(CACHE_ITUNES, 'r')
	CACHE_DICTION = json.loads(cache_file.read())
	cache_file.close()
except:
	CACHE_DICTION = {}


def params_unique_combination(base_url, params_d):
	alphabetized_keys = sorted(params_d.keys())
	res = []
	for k in alphabetized_keys:
		res.append("{}-{}".format(k, params_d[k]))
	return base_url + "_".join(res)


def get_from_itunes(search_word):
    base_url = "https://itunes.apple.com/search"
    parameters = {}
    parameters["term"] = search_word
    parameters["format"] = "json"
    unique_ident = params_unique_combination(base_url, parameters)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        response = requests.get(base_url, params=parameters)
        resp_dict = json.loads(response.text)
        write_file = open(CACHE_ITUNES, 'w')
        write_file.write(json.dumps(resp_dict))
        write_file.close()
        return resp_dict



################ other functions ###############

## check user input
def check_input(user_input):
    try:
        int(user_input)
        return True
    except:
        return False

## open url
def open_url(url):
    if url != "No URL":
        webbrowser.open_new(url)
        print("Preview at: " + url)
    else:
        print("No URL is available. ")



############### Part 3 & 4 ###############
if __name__ == "__main__":
 	# your control code for Part 4 (interactive search) should go here
    # first run, two options
    user_input = input("Enter a search term, or enter 'exit' to quit: ")

    while user_input != "exit":

        # check input is string or integer
        if check_input(user_input) == False:

            # make a request and group the results
            resp_data = get_from_itunes(user_input)
            search_results = resp_data["results"]
            instance_lst_dict = create_objects(search_results)

            # initiate indexing
            index_num = 1
            for category in instance_lst_dict:
                print(category) #Songs or Movies or Other Media
                for instance in instance_lst_dict[category]:
                    print(index_num, instance)
                    index_num += 1

        # input is an integer
        else:

            if int(user_input) not in range(1, (len(instance_lst_dict['SONGS']) + len(instance_lst_dict['MOVIES']) + len(instance_lst_dict['OTHER MEDIA'])+1)):
                print("Please enter a valid index number! ")
            else:
                index = int(user_input) - 1
                if int(user_input) <= len(instance_lst_dict['SONGS']):
                    preview_request = instance_lst_dict['SONGS'][index]
                elif int(user_input) > len(instance_lst_dict['SONGS']) and int(user_input) <= len(instance_lst_dict['SONGS']) + len(instance_lst_dict['MOVIES']):
                    index = index - len(instance_lst_dict['SONGS'])
                    preview_request = instance_lst_dict['MOVIES'][index]
                else:
                    index = index - (len(instance_lst_dict['SONGS']) + len(instance_lst_dict['MOVIES']))
                    preview_request = instance_lst_dict['OTHER MEDIA'][index]

                open_url(preview_request.preview)

        # prompt user for input again
        user_input = input("Enter an index number for more info, or another search term, or 'exit' to quit:  ")

    # end the program
    print("You have exited the search window. Bye!")
