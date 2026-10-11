from flask import Flask, render_template, request, jsonify
from deep_translator import MyMemoryTranslator
import urllib.parse

app = Flask(__name__)

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
        if not text:
            return jsonify({'translated': ''})
        # kama ni link kama https://...?q=hello, chukua q pekee
        if 'q=' in text:
            try:
                parsed = urllib.parse.urlparse(text)
                qs = urllib.parse.parse_qs(parsed.query)
                if 'q' in qs:
                    text = qs['q'][0]
            except:
                pass
        result = MyMemoryTranslator(source='en-US', target='sw-TZ').translate(text)
        return jsonify({'translated': result})
    except Exception as e:
        return jsonify({'translated': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run()
