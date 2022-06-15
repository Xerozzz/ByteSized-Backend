from cgi import test
import unittest
import requests
import json

# Class to start the Unit Test
class AddTest(unittest.TestCase):
    def test_1_getWebPage(self):
        URL = "http://127.0.0.1:5000/index"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 200)


# <--------------------------------------- User Related --------------------------------------->



# Function to unit Test registerUser API
    def test_2_registerUser(self):
        URL = "http://127.0.0.1:5000/register"
        testUser = {
            'username':'testuserHello',
            'email':'Hello@gmail.com',
            'password' : 'ThisIsASecret123!'
            }
        r = requests.post(URL, testUser)
        self.assertEqual(r.status_code, 200)

# Function to unit Test loginUser API
    def test_3_loginUser(self):
        URL = "http://127.0.0.1:5000/login"
        testUser = {
            'username':'jiajun is gay2',
            'email':'jiajunisgay1@gmail.com',
            'password':'jiajun is gayw'
            }
        r = requests.post(URL, testUser)
        self.assertEqual(r.status_code, 200)


# <--------------------------------------- Alias Related --------------------------------------->


# Function to unit Test aliasCreation API
    def test_4_AliasLink(self):
        URL = "http://127.0.0.1:5000/create"
        testREQ = {
            'original':'www.test.com',
            'alias' : 'dksjhlfls',
            'username' : 'jiajun is gay2',
            'tag': ''
            }
        r = requests.post(URL, testREQ)
        self.assertEqual(r.status_code, 200)

# Function to unit Test aliasUpdate API
    def test_5_AliasUpdate(self):
        URL = "http://127.0.0.1:5000/update"
        testJSON = {
            "username": "test",
            "alias": "facebook",
            "newAlias": "lkdjsnflksdhnjf",
            "newOriginal": "waljdhnk.ohngfks.com",
            "tag": "wda"
        }
        r = requests.put(
            URL, testJSON
        )
        self.assertEqual(r.status_code, 200)

# Function to unit Test aliasDeletion API
    def test_6_AliasDelete(self):
        URL = "http://127.0.0.1:5000/delete"
        r=requests.delete(URL, data={
            "username": "test",
            "alias": "reddit"
        })
        self.assertEqual(r.status_code, 200)

# Function to unit Test retrievingOriginalLink    (Still requires "Clicks" From mongo DB)
    def test_7_retrievingOriginalLink(self):
        URL = "http://127.0.0.1:5000/test/aws"
        r = requests.get(URL)
        self.assertEqual(r.status_code,200)

# Function to unit Test getAllLinks
    def test_8_getAllLinks(self):
        URL = "http://127.0.0.1:5000/test"
        r = requests.get(URL)
        print(r.text)
        self.assertEqual(r.status_code,200)
    

# <--------------------------------------- Stats Related --------------------------------------->


# Function to unit Test getStats
    def test_9_getStats(self):
        URL = "http://127.0.0.1:5000/test/aws/stats"
        testREQ = {
            "username" : "test",
            "alias" : "aws"
        }
        r = requests.get(URL, testREQ)
        self.assertEqual(r.status_code, 200)

# Function to unit Test getAllStats
    def test_10_getAllStats(self):
        URL = "http://127.0.0.1:5000/test/stats"
        testREQ = {
            "username" : "test"
        }
        r = requests.get(URL, testREQ)
        self.assertEqual(r.status_code, 200)

# Funciton to unit Test getDetailedStats  (Still requires "Clicks" From mongo DB)
    def test_11_getDetailedStats(self):
        URL = "http://127.0.0.1:5000/test/aws/stats/detailed"
        testREQ = {
            "username" : "test",
            "alias" : "aws"
        }
        r = requests.get(URL , testREQ)
        self.assertEqual(r.status_code, 200)
