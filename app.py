from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text','')
    to = data.get('to','sw')
    
    try:
        # Tumia MyMemory API direct
        url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(text)}&langpair=en|{to}"
        r = requests.get(url, timeout=10)
        j = r.json()
        translated = j['responseData']['translatedText']
        return jsonify({'translated': translated})
    except Exception as e:
        return jsonify({'translated': f"Error API: {str(e)}"})

if __name__ == '__main__':
    app.run()
