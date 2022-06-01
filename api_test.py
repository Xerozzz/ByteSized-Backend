import unittest
import requests
import json


class AddTest(unittest.TestCase):
    def test_1_getWebPage(self):
        URL = "http://127.0.0.1:5000/index"
        r = requests.get(URL)
        self.assertEqual(r.status_code, 200)
    def test_2_registerUser(self):
        URL = "http://127.0.0.1:5000/register"
        testUser = {'username':'testuserHello' , 'email' : 'Hello@gmail.com' , 'password' : 'ThisIsASecret123!'}
        r = requests.post(URL, testUser)
        self.assertEqual(r.status_code, 200)
    def test_3_loginUser(self):
        URL = "http://127.0.0.1:5000/login"
        testUser = {'username':'jiajun is gay2' , 'email' : 'jiajunisgay1@gmail.com' , 'password' : 'jiajun is gayw'}
        r = requests.post(URL, testUser)
        self.assertEqual(r.status_code, 200)
    def test_4_CreateLink(self):
        URL = "http://127.0.0.1:5000/create"
        testREQ = {'original':'www.test.com' , 'alias' : 'dksjhlfls' , 'username' : 'jiajun is gay2', 'tag': ''}