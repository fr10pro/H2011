# Filename: super_prompt_generator_single.py

from flask import Flask, request, render_template_string
import cohere
import os

# --- Initialize Flask ---
app = Flask(__name__)

# --- Cohere API Key ---
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "yA4Naz9dNcSD7WweJcTWBtVOaza2Xwo4jtJdwMpQ")
co = cohere.Client(COHERE_API_KEY)

# --- HTML Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Super Prompt Generator</title>
<style>
    body { font-family: Arial, sans-serif; background: #1a1a2e; color: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .container { max-width: 800px; width: 100%; text-align: center; }
    input, textarea { width: 100%; padding: 10px; margin: 10px 0; border-radius: 8px; border: none; }
    button { padding: 10px 20px; border: none; border-radius: 8px; background: #ff4d6d; color: white; font-weight: bold; cursor: pointer; }
    textarea { height: 250px; background: #2e2e3e; color: #fff; resize: none; }
</style>
</head>
<body>
<div class="container">
<h1>Super Pro Prompt Generator</h1>
<form method="POST">
    <input type="text" name="user_idea" placeholder="Enter your idea here..." required>
    <button type="submit">Generate Prompt</button>
</form>
{% if super_prompt %}
<h2>Generated Super Prompt:</h2>
<textarea readonly>{{ super_prompt }}</textarea>
{% endif %}
</div>
</body>
</html>
"""

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
    return render_template_string(HTML_TEMPLATE, super_prompt=super_prompt)

# --- Run Flask App ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
