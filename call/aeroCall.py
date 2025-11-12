# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv,find_dotenv

dotenv_path=find_dotenv()
load_dotenv(dotenv_path)

print(load_dotenv(dotenv_path))

def toolCall(contactNum,selfNum):
    return "callmade sucessfully"
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN") 

    print(account_sid,auth_token)
    client = Client(account_sid, auth_token)
    
    print("part5----------")
    call = client.calls.create(
        url="https://avocado-eagle-9088.twil.io/assets/groovy-vibe-427121.mp3",
        # twiml='<Response><Play>https://avocado-eagle-9088.twil.io/assets/groovy-vibe-427121.mp3</Play></Response>',
        to=contactNum,
        from_=selfNum
    )
    print("part5----------",call)
    print(call.sid)
    return call


if __name__ == "__main__":
    call=toolCall("+917987012077","+917224953542")
    print(call.sid)