from flask import Flask, request, render_template
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_trf")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entity', methods=['POST'])
def entity():
    text = ""

    # 1. First check manual text input
    manual_text = request.form.get('manual_text')
    if manual_text and manual_text.strip():
        text = manual_text.strip()

    # 2. If not, check file input
    elif 'file' in request.files:
        file = request.files['file']
        if file and file.filename:
            text = file.read().decode('utf-8', errors='ignore')

    # 3. If no input provided
    if not text:
        return render_template("index.html", html="<p>Please enter text or upload a file.</p>", text="")

    # Process with spaCy
    doc = nlp(text)
    html = displacy.render(doc, style="ent", page=False)
    rendered_html = f'<div class="card p-3 mt-2">{html}</div>'

    return render_template("index.html", html=rendered_html, text=text)

if __name__ == '__main__':
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
