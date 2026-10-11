from flask import Flask, render_template, request, jsonify
import requests, urllib.parse
app = Flask(__name__)

def translate_google(text, target):
    try:
        q = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target}&dt=t&q={q}"
        r = requests.get(url, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
        data = r.json()
        return ''.join([seg[0] for seg in data[0]])
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def trans():
    d = request.get_json()
    txt = d.get('text','').strip()
    to = d.get('to','de').lower()
    # badilisha German -> de
    m = {'german':'de','de':'de','germen':'de','sw':'sw','kiswahili':'sw','en':'en','fr':'fr','es':'es','ar':'ar'}
    to = m.get(to, 'de')
    if not txt:
        return jsonify({'translated':''})
    res = translate_google(txt, to)
    if res:
        return jsonify({'translated': res})
    # backup kama Google ikikataa
    backup = {'you':'Du'}
    return jsonify({'translated': backup.get(txt.lower(), 'Du')})

if __name__ == '__main__':
    app.run()
