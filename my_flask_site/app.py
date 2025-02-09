from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Configure your Gemini API key
genai.configure(api_key="")

load_dotenv()  # Load environment variables from .env file
# Configure the model
API_KEY = os.getenv("GEMINI_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Collecting form data
    name = request.form.get("name")
    domains = request.form.getlist("domain[]")
    projects = request.form.getlist("projects[]")
    java = request.form.get("java")
    python = request.form.get("python")
    sql = request.form.get("sql")

    # Creating the input prompt
    prompt = (
        f"Given the following details, recommend the best career paths:\n\n"
        f"Name: {name}\n"
        f"Interested Domains: {', '.join(domains)}\n"
        f"Completed Projects: {', '.join(projects)}\n"
        f"Skill Proficiency:\n"
        f"- Java: {java}\n"
        f"- Python: {python}\n"
        f"- SQL: {sql}\n\n"
        f"Provide a short and clear recommendation with career paths, including the scope of each job and its average salary."
    )

    try:
        model = genai.GenerativeModel('gemini-pro')  # Create model instance
        # Generate the response using Google Gen AI
        response = model.generate_content(prompt)  # Use generate_text instead
        
        # Log the full response for debugging
        print("Full API response:", response)

        # Extract the text from the response
        recommendation = response.text  # Access the text attribute

    except Exception as e:
        recommendation = f"An error occurred while generating the recommendation: {str(e)}"
        print(f"Error: {str(e)}")

    # Render the result in the HTML
    print("Recommendation: ", recommendation)   
    return render_template("index.html", recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
