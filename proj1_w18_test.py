## SI507 Winter2018
## 009 (Jie-wei Wu)
## Project 1
## Siyu Jia (uniqname: siyujia)

import unittest
import proj1_w18 as proj1
import json


############# Part 1 tests ############
class TestMedia(unittest.TestCase):

    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")

        # test Media constructor
        m3 = proj1.Media("Hey Jude", "The Beatles", "1968")
        self.assertEqual (m3.release_year, "1968")

        self.assertIsInstance(m3, proj1.Media)

        # check Media instances don't have special variables
        self.assertRaises(AttributeError, getattr, m3, 'rating')
        self.assertRaises(AttributeError, getattr, m3, 'genre')

        # test __str__ and __len__ methods
        self.assertEqual(m3.__str__(), "Hey Jude by The Beatles (1968)")
        self.assertEqual(m3.__len__(), 0)


class TestSong(unittest.TestCase):

    def testSongCons(self):
        s1 = proj1.Song("Hey Jude", "The Beatles", "1968",  "TheBeatles 1967-1970 (The Blue Album)", "Rock", 431333)
        s2 = proj1.Song()

        self.assertIsInstance(s1, proj1.Media)
        self.assertIsInstance(s1, proj1.Song)

        self.assertEqual(s1.title, "Hey Jude")
        self.assertEqual(s1.author, "The Beatles")
        self.assertEqual (s1.release_year, "1968")
        self.assertEqual (s1.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(s1.genre, "Rock")
        self.assertEqual(s1.track_len, 431333)
        # test default values
        self.assertEqual(s2.genre, "No Genre")
        self.assertEqual(s2.__len__(), 0)

        # check Media instances don't have special variables
        self.assertRaises(AttributeError, getattr, s1, 'rating')

        # test __str__ and __len__ methods
        self.assertEqual(s1.__str__(), "Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(s1.__len__(), 431)


class TestMovie(unittest.TestCase):

    def testMovieCons(self):
        mv1 = proj1.Movie("Jaws", "Steven Spielberg", "1975", "PG", 7451455)
        mv2 = proj1.Movie()

        self.assertIsInstance(mv1, proj1.Media)
        self.assertIsInstance(mv1, proj1.Movie)

        self.assertEqual(mv1.title, "Jaws")
        self.assertEqual(mv1.author, "Steven Spielberg")
        self.assertEqual (mv1.release_year, "1975")
        self.assertEqual (mv1.rating, "PG")
        self.assertEqual(mv1.movie_len, 7451455)
        # test default values
        self.assertEqual(mv2.rating, "No Rating")
        self.assertEqual(mv2.__len__(), 0)

        # check Media instances don't have special variables
        self.assertRaises(AttributeError, getattr, mv1, 'genre')

        # test __str__ and __len__ methods
        self.assertEqual(mv1.__str__(), "Jaws by Steven Spielberg (1975) [PG]")
        self.assertEqual(mv1.__len__(), 124)





############# Part 2 tests ############
class TestJson(unittest.TestCase):

    def testCreateObjects(self):

        # json_file = open("sample_json.json", "r")
        # json_list = json.load(json_file)
        # json_file.close()

        json_list = [{'wrapperType': 'track', 'kind': 'feature-movie', 'artistName': 'Steven Spielberg', 'collectionName': 'Steven Spielberg 7-Movie Director’s Collection', 'trackName': 'Jaws', 'releaseDate': '1975-06-20T07:00:00Z', 'trackTimeMillis': 7451455, 'contentAdvisoryRating': 'PG', 'trackViewUrl': 'https://itunes.apple.com/us/movie/jaws/id526768967?uo=4'}, {'wrapperType':
        'track', 'kind': 'song', 'artistName': 'The Beatles', 'collectionName': 'TheBeatles 1967-1970 (The Blue Album)', 'trackName': 'Hey Jude', 'releaseDate': '1968-08-26T07:00:00Z', 'trackTimeMillis': 431333, 'primaryGenreName': 'Rock', 'trackViewUrl': 'https://itunes.apple.com/us/album/hey-jude/400835735?i=400835962&uo=4'}, {'wrapperType': 'audiobook', 'artistName': 'Helen Fielding', 'collectionName': "Bridget Jones's Diary (Unabridged)", 'releaseDate':
        '2012-04-03T07:00:00Z', 'primaryGenreName': 'Fiction', 'collectionViewUrl': 'https://itunes.apple.com/us/audiobook/bridget-joness-diary-unabridged/id516799841?uo=4'}]

        for item in json_list:

            if "kind" in item:

                if item['kind'] == 'song':
                    item = proj1.Song(json = item)
                    ## test instance variables
                    self.assertEqual(item.title, "Hey Jude")
                    self.assertEqual(item.author, "The Beatles")
                    self.assertEqual(item.release_year, "1968")
                    self.assertEqual(item.album, "TheBeatles 1967-1970 (The Blue Album)")
                    self.assertEqual(item.genre, "Rock")
                    self.assertEqual(item.track_len, 431333)
                    # test __str__ and __len__ methods
                    self.assertEqual(item.__str__(), "Hey Jude by The Beatles (1968) [Rock]")
                    self.assertEqual(item.__len__(), 431)

                elif item['kind'] == 'feature-movie':
                    item = proj1.Movie(json = item)
                    ## test instance variables
                    self.assertEqual(item.title, "Jaws")
                    self.assertEqual(item.author, "Steven Spielberg")
                    self.assertEqual(item.release_year, "1975")
                    self.assertEqual(item.rating, "PG")
                    self.assertEqual(item.movie_len, 7451455)
                    # test __str__ and __len__ methods
                    self.assertEqual(item.__str__(), "Jaws by Steven Spielberg (1975) [PG]")
                    self.assertEqual(item.__len__(), 124)

            else:
                item = proj1.Media(json = item)
                self.assertEqual(item.title, "Bridget Jones's Diary (Unabridged)")
                self.assertEqual(item.author, "Helen Fielding")
                self.assertEqual(item.release_year, "2012")
                # test __str__ and __len__ methods
                self.assertEqual(item.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
                self.assertEqual(item.__len__(), 0)





############# Part 3 tests ############
class TestiTunesAPI(unittest.TestCase):

    def testQueries(self):

        # test common word: baby
        query1 = proj1.get_from_itunes("baby")
        search_results1 = query1["results"]
        results1_dict = proj1.create_objects(search_results1)

        # test if the number of results is within the default range (0-50)
        num1 = len(results1_dict['SONGS']) + len(results1_dict['MOVIES']) + len(results1_dict['OTHER MEDIA'])

        self.assertTrue(num1 >0 and num1 <= 50)


        # test less common words: moana
        query2 = proj1.get_from_itunes("moana")
        search_results2 = query2["results"]
        results2_dict = proj1.create_objects(search_results2)

        num2 = len(results2_dict['SONGS']) + len(results2_dict['MOVIES']) + len(results2_dict['OTHER MEDIA'])

        self.assertTrue(num2 >0 and num2 <= 50)


        # test nonsense queries: &@#!$
        query3 = proj1.get_from_itunes("&@#!$")
        search_results3 = query3["results"]
        results3_dict = proj1.create_objects(search_results3)

        num3 = len(results3_dict['SONGS']) + len(results3_dict['MOVIES']) + len(results3_dict['OTHER MEDIA'])

        self.assertTrue(num3 >= 0 and num3 <=50)


        # test blank
        query4 = proj1.get_from_itunes(" ")
        search_results4 = query4["results"]
        results4_dict = proj1.create_objects(search_results4)

        num4 = len(results4_dict['SONGS']) + len(results4_dict['MOVIES']) + len(results4_dict['OTHER MEDIA'])

        self.assertTrue(num4 == 0)


unittest.main()
