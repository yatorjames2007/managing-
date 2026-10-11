from flask import Flask, render_template, request, jsonify
import requests, urllib.parse
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/translate', methods=['POST'])
def trans():
    d=request.get_json()
    txt=d.get('text','').strip()
    to=d.get('to','sw').lower()
    m={'kiswahili':'sw','german':'de','arabic':'ar','french':'fr','sw':'sw','de':'de','ar':'ar'}
    to=m.get(to,'sw')
    q=urllib.parse.quote(txt)
    url=f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={to}&dt=t&q={q}"
    r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'}).json()
    res=''.join([x[0] for x in r[0]])
    return jsonify({'translated':res})
if __name__=='__main__':
    app.run()
