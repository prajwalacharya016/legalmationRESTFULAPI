# test_bucketlist.py
import unittest
import os
import json
import requests

class PlaintiffDefendant(unittest.TestCase):
    """This class represents the test cases"""
    def readXML(self, filename):
        with open(filename) as fd:
            legal_doc_xml = fd.read()
        return legal_doc_xml

    def setUp(self):
        """Define test variables and initialize app."""
        self.A = self.readXML('test_cases/A.xml')
        self.B = self.readXML('test_cases/B.xml')
        self.C = self.readXML('test_cases/C.xml')
        self.test = self.readXML('test_cases/test.xml')
        if os.path.exists("legaldoc.csv"):
            os.remove("legaldoc.csv")

    def test_add_correct_xml(self):
        """Test API can add data using xml(POST request)"""
        res_1 = requests.post('http://127.0.0.1:5002/add', data=self.A)
        self.assertEqual(res_1.status_code, 200)
        self.assertDictEqual(res_1.json(), {'STATUS': 'OK', 'plaintiff':'ANGELO ANGELES', 'defendant': 'HILL-ROM COMPANY'})

    def test_add_duplicate_xml(self):
        """Test API can add duplicate data using xml(POST request)"""
        res_1 = requests.post('http://127.0.0.1:5002/add', data=self.A)
        res_2 = requests.post('http://127.0.0.1:5002/add', data=self.A)
        self.assertEqual(res_2.status_code, 200)
        self.assertDictEqual(res_2.json(), {'STATUS':"Duplicate data, Data not saved to the csv"})

    def test_api_faulty_xml(self):
        """Test API response posting faulty xml (GET request)."""
        res_1 = requests.post('http://127.0.0.1:5002/add', data=self.test)
        self.assertEqual(res_1.status_code, 200)
        self.assertDictEqual(res_1.json(), {'STATUS': "Extreme apology, logic not good enough to parse the xml"})


    def test_get_all_data(self):
        """Test API can get all data"""
        res_1 = requests.post('http://127.0.0.1:5002/add', data=self.A)
        res_2 = requests.post('http://127.0.0.1:5002/add', data=self.B)
        res_3 = requests.post('http://127.0.0.1:5002/add', data=self.C)
        res_4 = requests.get("http://127.0.0.1:5002/getdata", data=self.test)
        self.assertListEqual(res_4.json(), [{'plaintiff': 'ANGELO ANGELES', 'defendant': 'HILL-ROM COMPANY'}, {'plaintiff': 'KUSUMA AMBELGAR', 'defendant': 'THIRUMALLAILLC'}, {'plaintiff': 'ALBA ALVARADO', 'defendant': 'LAGUARDIA ENTERPRISES'}])

    def tearDown(self):
        if os.path.exists("legaldoc.csv"):
            os.remove("legaldoc.csv")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
