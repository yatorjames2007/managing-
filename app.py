from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def trans():
    try:
        data = request.get_json()
        txt = data.get('text','').strip()
        to_raw = str(data.get('to','sw')).lower()

        mp = {'kiswahili':'sw','swahili':'sw','sw':'sw','en':'en','english':'en','french':'fr','fr':'fr','german':'de','de':'de','spanish':'es','es':'es','arabic':'ar','ar':'ar'}
        to = mp.get(to_raw, 'sw')

        if not txt:
            return jsonify({'translated': ''})

        # MyMemory - bure kabisa, hakuna limit kama Google
        url = f"https://api.mymemory.translated.net/get?q={txt}&langpair=en|{to}"
        r = requests.get(url, timeout=10)
        result = r.json()['responseData']['translatedText']
        return jsonify({'translated': result})
    except Exception as e:
        return jsonify({'translated': f"Error: {e}"})

if __name__ == '__main__':
    app.run()
