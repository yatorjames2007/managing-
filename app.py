from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)

def clean_lang(code):
    if not code:
        return 'en'
    code = str(code).lower().strip()
    if code == 'auto':
        return 'auto'
    # Chukua herufi 2 za kwanza tu: fr-BE -> fr, sw-TZ -> sw
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
        from_lang = clean_lang(data.get('from','auto'))

        if not text:
            return jsonify({'translated':''})

        # Force auto detection kwa source
        if from_lang == 'sw-tz' or from_lang == 'sw':
            from_lang = 'auto'

        result = GoogleTranslator(source='auto', target=to_lang).translate(text)
        return jsonify({'translated': result})
    except Exception as e:
        return jsonify({'translated': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run()
