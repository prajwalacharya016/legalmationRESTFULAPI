Note: *For the proper running of the test you need to have python2.7 in your machine*
  - Create a folder, legalmation_project_test
  - Copy your cloned repo into your folder
  - Now start virtualenv in legalmation_project_test
   - If you do not have virtualenv, pip install virtualenv
   - Go to folder where you created legalmation_project_test
   - Run: virtualenv legalmation_project_test
   - Lets choose python 2.7 as our interpreter
   - Run: virtualenv -p /usr/bin/python2.7 legalmation_project_test
   - Start virtual environment, Run: source legalmation_project_test/bin/activate
  - Now install the required packages *We could have requirements file but its not that too many so made part of this file*
   - pip install flask flask_restful requests xmltodict
  - Lets start the RESTful Api
   - cd legalmation_project_test/legalmationRESTFULAPI
   - python app.py
   
============================*****************===================================

Automatic Test cases:
  - In another terminal go to legalmation_project_test folder and start virtualenv
  - Run the test cases in legalmationRESTFULAPI
  - python legalmation_test.py
  - All test cases  *must* pass
=============================****************===================================

*The following QA Steps are more of my understanding of the issue and what properly runs as per how i solved the issue*
QA Steps:
  - Clone basic front-end I have created for testing of the Api
  - go to the legalmation_project_test
  - git clone https://github.com/prajwalacharya016/legalmationFrontEnd.git
  - In another terminal start the virtualenv
  - cd legalmation_project_test/legalmationFrontEnd
  - python upload.py
  - Open http://127.0.0.1:4555/
  - Should not get you any data as per now
  - There is an upload folder in frontend Api
  - Select one and click submit
  - Should add in result Result Data
  - Trying to add two of the same xml should give you duplicate error
  - Adding test.xml should give apologetic error message.
  - You have reached the end of the QA steps. Thanks for your patience and giving me opportunity to work on this wonderful project.

