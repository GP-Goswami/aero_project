
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

import os
import time
import json
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

def toolCall(contactNum, msg, selfNum):
    try:
    
        call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to=contactNum,
        from_=selfNum,
        )

        print("Call SID:", call.sid)

        # Poll until final status
        final_states = ["completed", "failed", "busy", "no-answer", "in-progress"]

        status = "queued"

        # Poll every second up to 15 seconds
        for i in range(15):
            status = client.calls(call.sid).fetch().status
            print("Checking status:", status)
            
            if status in final_states:
                break

            time.sleep(2)

        # Send a message
        message = client.messages.create(
            body=msg,
            to=contactNum,
            from_=selfNum
        )

        return {
            "call_sid": call.sid,
            "message_sid": message.sid,
            "call_status": status
        }
    # try:
    
        
    #     # Make a call
    #     call = client.calls.create(
    #         url="http://demo.twilio.com/docs/voice.xml",
    #         to=contactNum,
    #         from_=selfNum,
    #         status_callback="https://subacademically-pseudoprimitive-sona.ngrok-free.dev/call-status",
    #         status_callback_event=["initiated", "ringing", "answered", "completed"]
    #     )
    #     call_status = client.calls(call.sid).fetch().status
    #     print("Call SID:", call.sid,call_status)

    #     # Send a message
    #     message = client.messages.create(
    #         body=msg,
    #         to=contactNum,
    #         from_=selfNum
    #     )
    #     print("Message SID:", message.sid)

    #     return {"call_sid": call.sid, "message_sid": message.sid, "call_status": call_status}
    #     return {"call_sid": call.sid,  "call_status": call_status}
    
    except Exception as e:
        return {"call_status":f"failed{e}"}