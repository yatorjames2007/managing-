from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Map code yako -> jina kamili Google inataka
LANG_MAP = {
    'en': 'english',
    'sw': 'swahili',
    'fr': 'french',
    'de': 'german',
    'es': 'spanish',
    'ar': 'arabic',
    'zh': 'chinese',
    'hi': 'hindi',
    'it': 'italian',
    'pt': 'portuguese'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page')
def blank_page():
    return render_template('blank.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text','').strip()
        to_code = data.get('to','en').lower()[:2]
        
        if not text:
            return jsonify({'translated':''})

        # Tumia jina kamili
        to_lang = LANG_MAP.get(to_code, 'english')

        result = GoogleTranslator(source='auto', target=to_lang).translate(text)
        return jsonify({'translated': result})
    except Exception as e:
        return jsonify({'translated': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run()
