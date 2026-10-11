from flask import Flask, render_template, request
import requests
from urllib.parse import quote

app = Flask(__name__)

def translate_free(text, target_lang):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={quote(text)}"
        r = requests.get(url, timeout=10)
        data = r.json()
        translated = ''.join([s[0] for s in data[0] if s[0]])
        return translated
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    translated_text = None
    if request.method == 'POST':
        # Inachukua kutoka kwa hii form yako mpya
        text = request.form.get('link', '').strip()
        lang = request.form.get('lang', 'en').lower()[:2]

        if text:
            translated_text = translate_free(text, lang)
            if not translated_text:
                translated_text = "Error: Imefail, jaribu tena"

    return render_template('index.html', translated=translated_text)

@app.route('/translate', methods=['POST'])
def api_translate():
    # Bado inasupport JSON kama ukitaka
    try:
        data = request.get_json()
        text = data.get('text','').strip()
        to_code = data.get('to','en').lower()[:2]
        result = translate_free(text, to_code)
        return {'translated': result}
    except:
        return {'translated': 'Error'}

if __name__ == '__main__':
    app.run()
