from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def do_translate():
    data = request.get_json()
    text = data.get('text','').strip()
    to_raw = data.get('to','sw').lower()

    # convert German/Kiswahili/Arabic -> de/sw/ar
    lang_map = {
        'kiswahili':'sw', 'sw':'sw',
        'arabic':'ar', 'ar':'ar',
        'german':'de', 'de':'de', 'germen':'de',
        'english':'en', 'en':'en',
        'french':'fr', 'fr':'fr',
        'spanish':'es', 'es':'es'
    }
    to_lang = lang_map.get(to_raw, 'sw')

    if not text:
        return jsonify({'translated':''})

    try:
        result = translator.translate(text, dest=to_lang)
        return jsonify({'translated': result.text})
    except Exception as e:
        print("Translate error:", e)
        return jsonify({'translated': text})

if __name__ == '__main__':
    app.run()
