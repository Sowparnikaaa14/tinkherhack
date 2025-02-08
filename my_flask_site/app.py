from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure your Gemini API key
genai.configure(api_key="AIzaSyDC3dPz_t-w5lcwCPS2ZNIHieyL_2AJjMs")

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
        f"Provide a short and clear recommendation with career paths."
    )

    try:
        # Generate the response using Google Gen AI
        response = genai.generate_text(
            model="text-bison-001",  # Ensure you're using the right model
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=300,
        )

        # Extracting the generated text
        recommendation = response["candidates"][0]["output"]

    except Exception as e:
        recommendation = f"An error occurred while generating the recommendation: {str(e)}"

    # Render the result in the HTML
    print("Recommendation: ", recommendation)   
    return render_template("index.html", recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
