from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

mongoclient = MongoClient("mongodb://localhost:27017")
db = mongoclient['learnAI']
history = db['history']

app = Flask(__name__)
CORS(app)

@app.route("/api/test", methods=['POST'])
def process_message():
    # Get data sent to the endpoint
    message = request.args['message']

    return jsonify({"response": message+" bruhhh"})

@app.route("/api/getAIHistory", methods=['GET'])
def get_history():
    try:
        # Get only the 'ai_response' field from all the records
        records = history.find({}, {'ai_response': 1, '_id': 0})

        # Serialize the records using json_util
        records_json = json_util.dumps(records)

        # Return the records in JSON format
        return records_json

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/sendPrompt", methods=['POST'])
def chatbot():
    try:
        # Get the user input from the request body
        user_input = request.args['message']
        # Adding specific context or instructions to the user input
        augmented_input = f"Based on the following request, perform the required action:\n\n{user_input}"

        # Example of adding specific rules or context
        augmented_input += "\n\nIf the request is for generating questions, create 2 suitable math questions that will cover the all chapter and allow him to ace his exam."
        augmented_input += "\n\n List the questions in the format Question 1: <question 1> Question 2: <question 2>"

        client = openai.OpenAI(api_key=api_key)
        # Sending the augmented input to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role":"system",
                    "content":f"{augmented_input}"
                }
            ] ,  # Using augmented input as prompt
            max_tokens=1000
        )

        # Extract the response content
        message_content = response.choices[0].message.content if response.choices else "No response generated."

        # Insert the response into MongoDB
        inserted_record = history.insert_one({"user": user_input, "ai_response": "LearnAI: " + message_content})

        # Prepare the response data
        response_data = {
            "response": "LearnAI: " + message_content,
            "_id": str(inserted_record.inserted_id)  # Convert ObjectId to string for JSON serialization
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/api/checkAnswers", methods=['POST'])
def check_answers():
    try:
        user_answers = request.args['answers']
        # Fetch the entire conversation history from MongoDB
        conversation_history = list(history.find().sort("_id", -1))

        # Construct the conversation context for the AI
        conversation_context = " ".join([
            f"User: {ex['user']} LearnAI: {ex['ai_response']}"
            for ex in conversation_history
        ])

        # Construct a single prompt for all answers
        prompt = f"{conversation_context}\n\nProvide detailed corrections and suggest 1 additional exercise for the following questions and answers if the answers given are false:\n\n"
        prompt += f"User Answer: {user_answers}\n\n"


        client = openai.OpenAI(api_key=api_key)
        # Sending the augmented input to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"{prompt}"
                }
            ],  # Using augmented input as prompt
            max_tokens=1000
        )

        # Extract the response content
        message_content = response.choices[0].message.content if response.choices else "No response generated."

        # Insert the response into MongoDB
        inserted_record = history.insert_one({"user": user_answers, "ai_response": message_content})

        # Prepare the response data
        response_data = {
            "response": message_content,
            "_id": str(inserted_record.inserted_id)  # Convert ObjectId to string for JSON serialization
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)