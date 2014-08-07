from flask import Flask, request, json, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return 'adevc'


@app.route('/analyze_songs/', methods=['POST'])
def analyze_songs():
    payload = request.json
    with open('{0}.json'.format(payload['title']), 'w') as f:
        f.write(json.dumps(payload))
    return ''


@app.route('/pics/')
def pics():
    return send_file('./abc.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
