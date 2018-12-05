from __future__ import print_function
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

import os, xmltodict, sys, json, re, csv

app = Flask(__name__)
api = Api(app)

class DefendantPlaintiff:
	 """ Class for processing of revieved xml

    The object could be initialized with either xml or empty string


    Note:
        Proper way of initialization is empty string for retrieving data or xml string
        if need to add

    Args:
        xml (str): xml string for add, '' for updating

    Attributes:
        par (array): array of text parsed from xml
        code (orderedDict): ordered dict of key value parsed from xml
        plaintff_defendant (dict): dictionary containing plaintiff and
        							defendant data 
	
    """
	def __init__(self, xml):
		self.par =[]
		self.legal_doc = self.convertXMLtoDict(xml) if xml else {}
		self.plaintiff_defendant = {}

	def convertXMLtoDict(self,xml):
		"""Returns Ordered dictionary from xml string"""
		return xmltodict.parse(xml)

	def processJSON(self):
		"""
		Wrapper for JSON processing. From the initialized parameters, 
		it gets Plaintiff and Defendant data.

		Arguments:
			None takes all the attributes of the class

		Returns:
			dictionary containing plaintiff and defendants
		"""
	    pos_county_of = -1
	    pos_plaintiff = -1
	    pos_defendant = -1
	    self.traverseJSON(self.legal_doc)
	    regex = re.compile('[a-zA-Z]')
	    self.par= filter(regex.search, self.par)
	    #Traverse through filtered text array to retreive index positions
	    for text in self.par:
	        if "COUNTY OF " in text:
	            pos_county_of = self.par.index(text)
	        if "Plaintiff," in text:
	            pos_plaintiff = self.par.index(text)
	        if "Defendants." in text:
	            pos_defendant = self.par.index(text)

	    self.plaintiff_defendant['plaintiff'] = self.getPlaintiff(pos_county_of, pos_plaintiff, pos_defendant)
	    self.plaintiff_defendant['defendant'] = self.getDefendants(pos_county_of, pos_plaintiff, pos_defendant)
	    return self.plaintiff_defendant

	def traverseJSON(self,json):
		"""
		Recursive function going through all the keys of json and build text array
		
		Arguments:
			dict (dict): dictionary or sub dictionary to traverse

		Return:
			Nothing, Builds text string and save it in attributes	
		"""
	    if json and isinstance(json, dict):
	        for k, v in json.iteritems():
	            if k=="#text":
	            	self.par.append(v)
	            if isinstance(v, dict):
	                self.traverseJSON(v)
	            elif isinstance(v,list):
	                for w in v:
	                    self.traverseJSON(w)

	def getPlaintiff(self,pos_county_of,pos_plaintiff,pos_defendant):
		"""
		Logic for getting Plaintiff from text array
		
		Arguments:
			pos_county_of (int): Position of "COUNTY OF "
			pos_plaintiff(int): Position of "Paintiff,"
			pos_defendant(int): Position of "Defendant."

		Return:
			Plaintiff value 
		"""
		if len(self.par) and len(self.par)>pos_county_of:
			return self.par[pos_county_of+1].split(',')[0]
		else:
			return ''

	def getDefendants(self,pos_county_of,pos_plaintiff,pos_defendant):
		"""
		Logic for getting Defendant from text array
		
		Arguments:
			pos_county_of (int): Position of "COUNTY OF "
			pos_plaintiff(int): Position of "Paintiff,"
			pos_defendant(int): Position of "Defendant."

		Return:
			Defendant value 
		"""
		pos_of_vs=-1
		for text in self.par:
			if "v." in text or "vs." in text:
	  	  		pos_of_vs = self.par.index(text) if self.par.index(text)>pos_plaintiff and self.par.index(text)<pos_defendant else -1
	        	if pos_of_vs>-1:
	        		return self.par[pos_of_vs+1].split(',')[0] 
		return ''

	def writeToFile(self):
		"""Write the plaintiff value into csv"""
		f = open('legaldoc.csv','a')
		f.write(self.plaintiff_defendant['plaintiff']+","+self.plaintiff_defendant['defendant']+"\n")
		f.close()

	def getResults(self):
		"""Gets the plaintiff and Defendant data from csv"""
		data = []
		if os.path.exists('legaldoc.csv'):
			file=open( "legaldoc.csv", "r")
			reader = csv.reader(file)
			for line in reader:
				if ''.join(line).strip():
					print (line)
					t=[line[0]+line[1],line[0],line[1]]
					data.append(t)
			file.close()
		return data

class AddData(Resource):
	def post(self):
		"""
		Recieves the data called as post through route /add

		Gets data from the request, converts it into JSON,
		then processed to retrieve proper information

		Arguments:
			XML(xml): xml passed through rest call 

		returns:
			json containing STATUS, plaintiff, defendant on success
			error message on STATUS on invalid or not structured xml
		"""
		r = request.data
		ptdft = DefendantPlaintiff(r)
		result = ptdft.processJSON()
		if(result['defendant'] and result['plaintiff']):
			if result['plaintiff']+result['defendant'] not in map(lambda x:x[0], ptdft.getResults()):
				result['STATUS'] = "OK"
				ptdft.writeToFile()
			else:
				result = {'STATUS':"Duplicate data, Data not saved to the csv"}
			return jsonify(result)
		else:
			return jsonify({'STATUS': "Extreme apology, logic not good enough to parse the xml"})

class RetrieveData(Resource):
	"""
	Recieves the data called as get through route /getdata. Returns array of data

	Arguments:
		None

	returns:
		json containing arrays of plaintiff and defendant present in csv
	"""
	def get(self):
		ptdft = DefendantPlaintiff('')
		return jsonify(map(lambda x:{'plaintiff': x[1], 'defendant': x[2]}, ptdft.getResults()))
		
api.add_resource(AddData, '/add')
api.add_resource(RetrieveData, '/getdata')


if __name__ == '__main__':
	 app.run(port='5002')