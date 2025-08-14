from flask import Flask, render_template, request
import cohere
import os

# --- Initialize Flask ---
app = Flask(__name__)

# --- Cohere API Key (use Render environment variable for security) ---
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "your_cohere_api_key_here")
co = cohere.Client(COHERE_API_KEY)

# --- Generate Super Prompt Function ---
def generate_super_prompt(user_idea):
    master_prompt = f"""
You are an elite AI prompt engineer and creative director.
Your mission: transform ANY user idea into a highly detailed,
professionally structured, and stylistically unique prompt for an AI model.

Project Style Guidelines:

Tone: Futuristic + Premium + Minimalist elegance

Output Structure:

1. Role Assignment (expert persona)
2. Creative Context & Inspiration
3. Detailed Task Instructions
4. Technical & Formatting Constraints
5. Unique Style Elements

Vocabulary: vivid, cinematic, and high-imagery language
Always inject subtle metaphor or storytelling
Ensure instructions are model-friendly and unambiguous

Input: "{user_idea}"

Output must be a complete AI-ready prompt that:
- Can be used directly in any AI text/image model
- Captures a consistent “signature style” for the project
- Has no filler words, only high-value instructions
- Feels tailor-made and premium

Begin transformation now.
"""
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=master_prompt,
        max_tokens=400
    )
    return response.generations[0].text.strip()

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def home():
    super_prompt = ""
    if request.method == "POST":
        user_idea = request.form.get("user_idea", "")
        if user_idea:
            super_prompt = generate_super_prompt(user_idea)
    return render_template("index.html", super_prompt=super_prompt)

# --- Run Flask App ---
if __name__ == "__main__":
    app.run(debug=True)
