from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote

app = Flask(__name__)

def translate_free(text, target_lang):
    try:
        m = {'kiswahili':'sw','swahili':'sw','english':'en','french':'fr','german':'de','spanish':'es','arabic':'ar'}
        target_lang = m.get(target_lang.lower(), target_lang.lower()[:2])
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={quote(text)}"
        r = requests.get(url, timeout=10)
        data = r.json()
        return ''.join([s[0] for s in data[0] if s[0]])
    except:
        return "Error"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_api():
    data = request.get_json()
    text = data.get('text','')
    lang = data.get('to','sw')
    result = translate_free(text, lang)
    return jsonify({'translated': result})

if __name__ == '__main__':
    app.run()
