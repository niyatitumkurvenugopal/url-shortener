# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

url_mappings = {}

@app.route('/')
def index():
    return render_template('index.html', url_mappings=url_mappings)

@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    original_url = request.form.get('original_url')
    if original_url:
        # Generate a unique short code for the URL (you can use a more sophisticated method)
        short_code = str(len(url_mappings) + 1)
        short_url = f"http://localhost:5000/{short_code}"

        url_mappings[short_code] = original_url
    return redirect(url_for('index'))

@app.route('/edit_url/<short_code>', methods=['POST'])
def edit_url(short_code):
    updated_url = request.form.get('updated_url')
    if short_code in url_mappings and updated_url:
        url_mappings[short_code] = updated_url
    return redirect(url_for('index'))

@app.route('/delete_url/<short_code>')
def delete_url(short_code):
    url_mappings.pop(short_code, None)
    return redirect(url_for('index'))

@app.route('/<short_code>')
def redirect_to_original(short_code):
    original_url = url_mappings.get(short_code)
    if original_url:
        return redirect(original_url)
    return f"URL not found for code: {short_code}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
