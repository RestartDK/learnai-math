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
        prompt = f"Create 5 suitable math questions for the topic '{topic}' that will cover all chapters and allow a student to ace their exam."

        # Sending the prompt to the OpenAI API
        response = openai.Completion.create(
            model="gpt-4-1106-preview",
            prompt=prompt,
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
        user_answers = request.json  # Assuming answers are sent as a JSON payload
        corrections = {}

        for question, user_answer in user_answers.items():
            expected_answer = questions_and_answers.get(question, "No answer available")
            correction = generate_correction_and_exercise(question, user_answer, expected_answer)
            corrections[question] = correction

        return jsonify({"corrections": corrections})

    except Exception as e:
        return jsonify({"error": str(e)})

def generate_correction_and_exercise(question, user_answer, expected_answer):
    # Construct a prompt for OpenAI
    prompt = f"Question: {question}\nUser Answer: {user_answer}\nExpected Answer: {expected_answer}\n\nProvide a detailed correction of the user's answer and suggest additional exercises for practice:"

    try:
        # Sending the prompt to the OpenAI API
        response = openai.Completion.create(
            model="gpt-4-1106-preview",
            prompt=prompt,
            max_tokens=200  # Adjust as needed
        )

        # Extracting the generated response
        generated_response = response.choices[0].message.content if response.choices else "No response generated."

        return generated_response
    except Exception as e:
        return f"Error generating correction: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)

