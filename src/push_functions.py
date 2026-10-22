from dotenv import load_dotenv
import requests
import os


load_dotenv(override=True)

def push(text):
    requests.post(
         "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

def record_user_details(email, name="name is not provided", notes="not provided"):
    push(f"There is an interest from {name} with email {email} and notes {notes}")
    return {"recorded": "OK"}

def record_unknown_question(question):
    push(f"Taking a note of this question {question} that I couldn't answer")
    return {"recorded": "OK"}
