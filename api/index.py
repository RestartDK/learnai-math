from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = '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'

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/generateQuestions", methods=['GET'])
def generate_questions():
    try:
        # Get the grade level and math topic from the request
        grade_level = request.args.get('grade', 'middle school')
        math_topic = request.args.get('topic', '')

        # Building the prompt to get a list of subtopics
        topic_prompt = f"List subtopics for the math topic '{math_topic}' suitable for a {grade_level} student."

        # Generating the response for subtopics
        topic_response = openai.Completion.create(
            engine="text-davinci-004",  # or "gpt-4" based on your access
            prompt=topic_prompt,
            max_tokens=50
        )

        subtopics = topic_response.choices[0].text.strip()

        questions = []
        for _ in range(5):  # Adjust range for the desired number of questions
            # Building the prompt for questions
            question_prompt = f"Create a math question for {grade_level} students on the topic '{math_topic}'."

            # Generating the response for questions
            question_response = openai.Completion.create(
                engine="text-davinci-004",  # or "gpt-4" based on your access
                prompt=question_prompt,
                max_tokens=100
            )

            question = question_response.choices[0].text.strip()
            questions.append(question)

        return jsonify({"subtopics": subtopics, "questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)})
    

if __name__ == "__main__":
    app.run(debug=True)


