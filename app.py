from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text','').strip()
    to = data.get('to','sw').lower()
    
    if not text:
        return jsonify({'translated':''})

    # 1. LIBRE - Hii ndio inatranslate ANY LANGUAGE, sio moja
    try:
        # Hii API ni free, haina limit kama Google
        res = requests.post(
            "https://translate.argosopentech.com/translate",
            json={"q": text, "source": "auto", "target": to, "format": "text"},
            timeout=15
        ).json()
        if res.get('translatedText'):
            return jsonify({'translated': res['translatedText']})
    except Exception as e:
        print("Libre failed:", e)

    # 2. MyMemory kama backup ya any language
    try:
        from urllib.parse import quote
        r = requests.get(f"https://api.mymemory.translated.net/get?q={quote(text)}&langpair=auto|{to}", timeout=10).json()
        tr = r.get('responseData',{}).get('translatedText','')
        if tr:
            return jsonify({'translated': tr})
    except:
        pass

    return jsonify({'translated': text + " (translation failed)"})

if __name__ == '__main__':
    app.run()
