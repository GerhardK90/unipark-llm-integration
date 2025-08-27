from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import csv
from datetime import datetime
import os

# Initialize Flask app and OpenAI client
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
client = OpenAI(api_key='sk-proj-xxxx')  # Replace with your API key

# Function to send prompt to OpenAI and get the response (updated for openai>=1.0.0)
# Function to send prompt to OpenAI and get the response (updated for openai>=1.0.0)
def get_chatgpt_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response_data = completion.model_dump()  # Convert the response to a dictionary
    return response_data["choices"][0]["message"]["content"]

# Ensure the CSV file and headers are set up
CSV_FILE_PATH = "responses.csv"
if not os.path.exists(CSV_FILE_PATH):
    with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["questionnaire_id", "prompt", "response", "timestamp"])

# Endpoint for Unipark to submit a single prompt
@app.route('/submit_prompt', methods=['POST', 'OPTIONS'])
def submit_prompt():
    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        print("Received OPTIONS request.")
        return '', 200

    # Print out the request data for debugging
    print("Received POST request.")
    print("Request data:", request.data)

    data = request.get_json()
    print("Parsed JSON data:", data)

    # Extract questionnaire ID and prompt from the request
    questionnaire_id = data.get("questionnaire_id")
    prompt = data.get("prompt")

    if not questionnaire_id or not prompt:
        print("Error: Missing questionnaire_id or prompt.")
        return jsonify({"error": "Both questionnaire_id and prompt are required"}), 400

    # Get response from ChatGPT
    try:
        response = get_chatgpt_response(prompt)
    except Exception as e:
        print("Error communicating with ChatGPT:", e)
        return jsonify({"error": str(e)}), 500

    # Save questionnaire_id, prompt, response, and timestamp to CSV
    timestamp = datetime.utcnow().isoformat()
    with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([questionnaire_id, prompt, response, timestamp])

    print(f"Saved to CSV: {questionnaire_id}, {prompt}, {response}, {timestamp}")

    # Return only the response to Unipark
    return jsonify({"response": response}), 200

# Run the app on all available network interfaces
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
