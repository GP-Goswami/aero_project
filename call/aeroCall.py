# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def toolCall(contactNum,selfNum):
    account_sid = os.environ["Env:TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["Env:TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml="<Response><Say>Ahoy, World</Say></Response>",
        to=str(contactNum),
        from_=str(selfNum),
    )
    return call

if __name__ == "__main__":
    call=toolCall(12345,7224953542)
    print(call.sid)