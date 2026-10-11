from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
app = Flask(__name__)
@app.route('/')
def home(): return render_template('index.html')
@app.route('/translate', methods=['POST'])
def trans():
    data=request.get_json()
    txt=data.get('text',''); to=data.get('to','sw')[:2]
    result=GoogleTranslator(source='auto', target=to).translate(txt)
    return jsonify({'translated':result})
if __name__=='__main__': app.run()
