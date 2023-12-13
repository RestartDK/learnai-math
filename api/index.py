from flask import Flask, request, jsonify
import openai
import dotenv
import os
from flask_cors import CORS

from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Temporary storage for questions and answers
questions_and_answers = {}

@app.route("/api/generateQuestions", methods=['POST'])
def generate_questions():
    try:
        # Get the topic from the request body
        data = request.json
        topic = data.get('topic', 'default topic')

        # Construct a prompt for OpenAI to generate questions

        augmented_input = f"Based on the following request, perform the required action:\n\n{user_input}"

        # Example of adding specific rules or context
        augmented_input += "\n\nIf the request is for generating questions, create 5 suitable math questions that will cover the all chapter and allow him to ace his exam."
        augmented_input += "\nIf the request is for correcting answers, provide the correct answers and explanations. The answers should be very detailed and similar to if they were handwritten"

        # Sending the prompt to the OpenAI API
        response = openai.Completion.create(
            model="gpt-4-1106-preview",
            prompt=augmented_input,
            max_tokens=500  # Adjust as needed
        )

        # Extracting the generated questions
        generated_questions = response.choices[0].message.content if response.choices else "No questions generated."

        # Assuming each line in generated_questions is a separate question
        for question in generated_questions.split('\n'):
            questions_and_answers[question] = "Expected answer"  # Placeholder for expected answers

        return jsonify({"questions": generated_questions})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/checkAnswers", methods=['POST'])
def check_answers():
    try:
        user_answers = request.json

        # Construct a single prompt for all answers
        prompt = "Provide detailed corrections and suggest additional exercises for the following questions and answers:\n\n"
        for question, user_answer in user_answers.items():
            expected_answer = questions_and_answers.get(question, "No answer available")
            prompt += f"Question: {question}\nUser Answer: {user_answer}\nExpected Answer: {expected_answer}\n\n"

        response = openai.Completion.create(
            model="gpt-4-1106-preview",
            prompt=prompt,
            max_tokens=1000
        )

        generated_response = response.choices[0].message.content if response.choices else "No response generated."

        return jsonify({"corrections": generated_response})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)

