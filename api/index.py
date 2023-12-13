from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os
from flask_cors import CORS

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/api/test", methods=['POST'])
def process_message():
    # Get data sent to the endpoint
    message = request.args['message']

    return jsonify({"response": message+" bruhhh"})

@app.route("/api/sendPrompt", methods=['POST'])
def chatbot():
    try:
        # Get the user input from the request body
        user_input = request.args['message']
        print(user_input)
        # Adding specific context or instructions to the user input
        augmented_input = f"Based on the following request, perform the required action:\n\n{user_input}"

        # Example of adding specific rules or context
        augmented_input += "\n\nIf the request is for generating questions, create 5 suitable math questions that will cover the all chapter and allow him to ace his exam."
        augmented_input += "\nIf the request is for correcting answers, provide the correct answers and explanations. The answers should be very detailed and similar to if they were handwritten"

        client = openai.OpenAI(api_key=api_key)
        # Sending the augmented input to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role":"system",
                    "content":f"{augmented_input}"
                }
            ] ,  # Using augmented input as prompt
            max_tokens=1000
        )

        # Extracting the generated response
        # generated_content = response.choices[0].text.strip() if response.choices else "No response generated."

        return {"response": response.choices[0].message.content}

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)