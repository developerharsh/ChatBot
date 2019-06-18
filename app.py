
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply



app = Flask(__name__)

@app.route("/",methods=['POST'])

def hello():
	resp = MessagingResponse()
	response = detect_intent_from_text("hi", 12314)
	resp.message(response.fulfillment_text)
	return str(resp)

@app.route("/sms", methods=['POST'])
def sms_reply():
    # Fetch the message
    #print(request.form)
    msg = request.form.get('Body')
    sender=request.form.get('From')
    # Create reply
    resp = MessagingResponse()
    #resp.message("You said: {}".format(msg))
    #resp.message("You said: {}".format(msg)).media("https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80")
    x,y=fetch_reply(msg,sender)
    if y=="number":
    	resp.message(x)
    elif y=="images":
    	resp.message("Your image").media(x)
    else:
    	resp.message(x)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)