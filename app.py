from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

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

        mp = {'kiswahili':'sw','swahili':'sw','sw':'sw','en':'en','english':'en','french':'fr','fr':'fr','german':'de','de':'de','spanish':'es','es':'es','arabic':'ar'}
        to = mp.get(to_raw, 'sw')

        if not txt:
            return jsonify({'translated': ''})

        result = GoogleTranslator(source='auto', target=to).translate(txt)
        return jsonify({'translated': result})
    except Exception as e:
        return jsonify({'translated': f"Error: {e}"})

if __name__ == '__main__':
    app.run()
