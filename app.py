from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator, MyMemoryTranslator
import time

app = Flask(__name__)

LANG_MAP_GOOGLE = {
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

LANG_MAP_MYMEMORY = {
    'en': 'en-US',
    'sw': 'sw-TZ',
    'fr': 'fr-FR',
    'de': 'de-DE',
    'es': 'es-ES',
    'ar': 'ar-SA',
    'zh': 'zh-CN',
    'hi': 'hi-IN',
    'it': 'it-IT',
    'pt': 'pt-PT'
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

        to_google = LANG_MAP_GOOGLE.get(to_code, 'english')
        to_mymem = LANG_MAP_MYMEMORY.get(to_code, 'en-US')

        # 1. Jaribu Google kwanza
        try:
            result = GoogleTranslator(source='auto', target=to_google).translate(text)
            return jsonify({'translated': result})
        except Exception as e:
            # 2. Google ikikataa juu ya Too many requests, tumia MyMemory (haina limit)
            if 'too many' in str(e).lower() or 'server error' in str(e).lower() or 'request' in str(e).lower():
                result2 = MyMemoryTranslator(source='en-US', target=to_mymem).translate(text)
                return jsonify({'translated': result2})
            else:
                # Kwa error zingine kama sw, tumia MyMemory direct
                result2 = MyMemoryTranslator(source='en-US', target=to_mymem).translate(text)
                return jsonify({'translated': result2})

    except Exception as e:
        return jsonify({'translated': f"Please wait 30 seconds and try again. ({str(e)[:80]})"})

if __name__ == '__main__':
    app.run()
