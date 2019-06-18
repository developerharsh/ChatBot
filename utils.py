import os
import requests
from pymongo import MongoClient
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newbot-nlafkd"

client=MongoClient("mongodb+srv://test:test@cluster0-oiqiu.mongodb.net/test?retryWrites=true&w=majority")
db=client.get_database("users")
records=db.user_pref

def get_verify(parameters,session_id):
	#print(parameters)
	#client.topic = parameters.get('news_type')
	#client.language = parameters.get('language')
	#client.location = parameters.get('geo-country')
	sessstr=(str)(session_id)
	cont_code={
		"India":"in",
		"india":"in",
		"Afghanistan":"af",
		"afghanistan":"af",
		"America":"as",
		"america":"as",
		"Australia":"au",
		"australia":"au",
		"Bhutan":"bt",
		"bhutan":"bt",
		"Canada":"ca",
		"canada":"ca",
		"China":"cn",
		"china":"cn",
		"United States":"un",
		"united states":"un"
	}
	number=parameters.get('phone-number')
	cnty=parameters.get('geo-country')
	inctr=cont_code.get(cnty);
	print(number)
	print(inctr)

	#**********************************  DataBase Code  **************************************************
	obj=records.find_one({"session_id":sessstr})
	if obj==None:
		new_obj={
    		"session_id":sessstr,
    		"numbers":[number],
    		"countries":[inctr]
		}
		records.insert_one(new_obj)
	else:
		obj['numbers'].append(number)
		obj['countries'].append(inctr)
		records.delete_one({"session_id":sessstr})
		records.insert_one(obj)
	#*****************************************************************************************************
	if inctr == None:
		url="http://apilayer.net/api/validate?access_key=496d8b4cbe14c507d68ac4c7b0e1f3b3&number="+number+"&country_code=in&format=1"
	else:
		url="http://apilayer.net/api/validate?access_key=496d8b4cbe14c507d68ac4c7b0e1f3b3&number="+number+"&country_code="+inctr+"&format=1"
	r=requests.get(url)
	print(url);
	if r.json()["valid"]:
		stri="Valid: "+(str)(r.json()["valid"])+"\nNumber: "+r.json()["international_format"]+"\nLocation: "+r.json()["country_code"]+", "+r.json()["location"]
	else:
		stri="Invalid Number"
	return stri

def detect_intent_from_text(text, session_id, language_code='en'):
	
	session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
	text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
	query_input = dialogflow.types.QueryInput(text=text_input)
	response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
	
	return response.query_result

def get_images(parameters,session_id):
	breed=parameters.get('dogs')
	url="https://dog.ceo/api/breed/"+breed+"/images"
	r=requests.get(url)
	img=r.json()["message"][0]
	return img


def fetch_reply(msg, session_id):

	response = detect_intent_from_text(msg, session_id)
	#print(response.intent.display_name)
	if response.intent.display_name == 'phone_type':
		
		verify = get_verify(dict(response.parameters),session_id)
		#for row in verify:
		#	news_str += "\n\n{}\n\n{}\n\n".format(row['title'],	row['link'])
		return verify,"number"

	elif response.intent.display_name == 'dog_breeds':
		image=get_images(dict(response.parameters),session_id)
		return image,"images"
	else:
		return response.fulfillment_text,""