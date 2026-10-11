from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator, MyMemoryTranslator

app = Flask(__name__)

def clean_lang(code):
    if not code: return 'en'
    code = str(code).lower().strip()
    if code == 'auto': return 'auto'
    return code.split('-')[0].split('_')[0][:2]

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
        to_lang = clean_lang(data.get('to','sw'))

        if not text:
            return jsonify({'translated':''})

        # 1. Jaribu Google kwanza
        try:
            result = GoogleTranslator(source='auto', target=to_lang).translate(text)
            return jsonify({'translated': result})
        except Exception as e:
            err = str(e).lower()
            # Kama Google imeblock, tumia MyMemory
            if 'too many' in err or 'server error' in err or 'request' in err:
                # MyMemory haina limit
                my_from = 'en' if to_lang!= 'en' else 'sw'
                # Kama text ni kiswahili, anza na sw
                result2 = MyMemoryTranslator(source='en-US', target=to_lang).translate(text)
                if not result2 or result2 == text:
                    result2 = MyMemoryTranslator(source='auto', target=to_lang).translate(text)
                return jsonify({'translated': result2})
            else:
                raise e

    except Exception as e:
        return jsonify({'translated': f"Subiri 1 min kisha jaribu tena. Google imezidiwa: {str(e)[:100]}"})

if __name__ == '__main__':
    app.run()
