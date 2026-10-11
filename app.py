from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

# Dictionary ya akiba kama internet ikikataa
BACKUP = {
    "how are you": {"sw": "Habari, unaendeleaje?", "ar": "كيف حالك", "fr": "Comment ça va?", "de": "Wie geht es dir?", "es": "¿Cómo estás?"},
    "hello": {"sw": "Habari", "ar": "مرحبا", "fr": "Bonjour", "de": "Hallo", "es": "Hola"}
}

def translate_google_free(text, target):
    try:
        # Hii ni API ya Google ya siri - bure, haina limit kubwa
        q = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target}&dt=t&q={q}"
        r = requests.get(url, timeout=8, headers={'User-Agent':'Mozilla/5.0'})
        data = r.json()
        return ''.join([x[0] for x in data[0]])
    except:
        return None

def translate_mymemory(text, target):
    try:
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|{target}&de=yatorjames2007@gmail.com"
        r = requests.get(url, timeout=8)
        return r.json()['responseData']['translatedText']
    except:
        return None

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

        low = txt.lower()
        # Jaribu Google ya siri kwanza
        res = translate_google_free(txt, to)
        if res and "MYMEMORY WARNING" not in res and "Error" not in res:
            return jsonify({'translated': res})

        # Jaribu MyMemory na email
        res2 = translate_mymemory(txt, to)
        if res2 and "MYMEMORY WARNING" not in res2:
            return jsonify({'translated': res2})

        # Backup dictionary
        if low in BACKUP and to in BACKUP[low]:
            return jsonify({'translated': BACKUP[low][to]})

        return jsonify({'translated': res or res2 or "Try again in 1 min - limit imeisha"})
    except Exception as e:
        return jsonify({'translated': f"Error: {e}"})

if __name__ == '__main__':
    app.run()
