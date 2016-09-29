from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from nltk.tokenize import sent_tokenize

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/analyze_review', methods=['GET', 'POST'])
def analyze_review():
    review = ''
    results = {}

    if request.method == 'GET':
        review = request.args.get('review')
    elif request.method == 'POST':
        review = request.json['review']

    if review != '':
        sentences = sent_tokenize(review)

        overall_compound = 0.0;

        for sentence in sentences:
            sa = vaderSentiment(sentence)
            results[sentence] = sa
            overall_compound += float(sa['compound'])

        return jsonify(overall_compound = overall_compound, sentiments=results)

@app.route('/analyze_sentences', methods=['GET', 'POST'])
def analyze_sentences():
    review = ''
    results = {}
    sentences = []
    if request.method == 'GET':
        sentences = request.args.getlist('sentences')
    elif request.method == 'POST':
        sentences = request.json['sentences']

    if len(sentences) > 0:
        overall_compound = 0.0;

        for sentence in sentences:
            sa = vaderSentiment(sentence)
            results[sentence] = sa
            overall_compound += float(sa['compound'])

        return jsonify(overall_compound = overall_compound, sentiments=results)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3008, threaded=True)
