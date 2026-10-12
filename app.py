from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OFFLINE = {
    'how are you': {'sw':'Habari yako?','ar':'كيف حالك؟','de':'Wie geht es dir?','fr':'Comment ça va?','en':'How are you'},
    'how are you?': {'sw':'Habari yako?','ar':'كيف حالك؟','de':'Wie geht es dir?'},
    'welcome': {'sw':'Karibu','ar':'أهلاً وسهلاً','de':'Willkommen','fr':'Bienvenue'},
    'thank you': {'sw':'Asante','ar':'شكرا لك','de':'Danke','fr':'Merci'},
    'you': {'sw':'wewe','ar':'أنت','de':'Du','fr':'toi'},
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def trans():
    data = request.get_json() or {}
    txt = data.get('text','').strip()
    to = data.get('to','sw').lower()[:2]
    if not txt:
        return jsonify({'translated':''})
    low = txt.lower()
    if low in OFFLINE and to in OFFLINE[low]:
        return jsonify({'translated': OFFLINE[low][to]})
    try:
        r = requests.get(f"https://api.mymemory.translated.net/get?q={txt}&langpair=en|{to}", timeout=7).json()
        t = r.get('responseData',{}).get('translatedText','')
        if t and 'MYMEMORY' not in t and 'LIMIT' not in t:
            return jsonify({'translated': t})
    except:
        pass
    return jsonify({'translated': OFFLINE.get(low,{}).get(to, txt)})
