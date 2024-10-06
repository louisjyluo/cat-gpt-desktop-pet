from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get OpenAI API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
api_request_counter = 0

class catgptAI():
    def chat(msg):
        global api_request_counter
        api_request_counter += 1
        print(f"API Request Count: {api_request_counter}")
        
        try:
            # Get the user's message from the request body
            user_message = msg
            user_message = user_message + "Instruction: make the response sound like a cat replied and not have it be over 200 words NO MATTER WHAT."
            
            # Make a request to the OpenAI API
            response = client.chat.completions.create(model="gpt-4o",  # or gpt-3.5-turbo
            messages=[
                {"role": "user", "content": user_message}
            ])

            # Extract the assistant's response
            assistant_message = response.choices[0].message.content
            
            # Return the assistant's message as a JSON response
            return assistant_message

        except Exception as e:
            print(f"Error: {e}")
            return "Error: Something went wrong"