from flask import Flask, render_template, request, jsonify
import requests, urllib.parse
app = Flask(__name__)

BACKUP = {
    'you': {'sw':'wewe','de':'Du','ar':'أنت','en':'you'},
    'welcome': {'sw':'karibu','de':'Willkommen','ar':'أهلاً وسهلاً','en':'welcome'},
    'come here': {'sw':'kuja hapa','de':'komm her','ar':'تعال هنا','en':'come here'},
}

def google_trans(text, target):
    try:
        q = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target}&dt=t&q={q}"
        r = requests.get(url, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
        j = r.json()
        return ''.join([x[0] for x in j[0]])
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def trans():
    d = request.get_json()
    txt = d.get('text','').strip()
    to_raw = d.get('to','sw').lower()
    mp = {'kiswahili':'sw','sw':'sw','arabic':'ar','ar':'ar','german':'de','de':'de','english':'en','en':'en','french':'fr','fr':'fr'}
    to = mp.get(to_raw,'sw')
    if not txt: return jsonify({'translated':''})
    low = txt.lower()
    if low in BACKUP and to in BACKUP[low]:
        return jsonify({'translated': BACKUP[low][to]})
    res = google_trans(txt, to)
    if res: return jsonify({'translated': res})
    return jsonify({'translated': txt})

if __name__ == '__main__':
    app.run()
