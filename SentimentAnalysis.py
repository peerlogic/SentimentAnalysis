from flask import Flask, render_template, request, jsonify
from flask_api import status
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from nltk.tokenize import sent_tokenize
import colorsys

app = Flask(__name__)


def get_hsl(val):
    value = float(val)
    H = int((value + 1) * 120/2 - 1)
    # spectrum is red (0.0), orange, yellow, green, blue, indigo, violet (0.9)
    # hue = percent * (end_hue - start_hue) + start_hue
    # lightness = 0.5
    # saturation = 1
    # r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    S = 70
    L = 35

    return "hsl(" + str(H) + ", " + str(S) + "%, " + str(L) + "%)"

@app.route('/developer', methods=['GET'])
def developer():
    return render_template("developer.html")

@app.route('/instructor', methods=['GET'])
def instructor():
    return render_template("instructor.html")

@app.route('/visualize_sentiment', methods=['GET', 'POST'])
def visualize_sentiment():
    if request.method == 'GET':
        review = request.args.get('review')
    elif request.method == 'POST':
        review = request.json['review']

    if review != '':
        sentences = sent_tokenize(review)

        overall_compound = 0.0;

        for sentence in sentences:
            sa = vaderSentiment(sentence)
            sentiment = round(float(sa['compound']),1)
            review = review.replace(sentence, '<font style="color:' + get_hsl(sa['compound']) + ';">' + sentence + '[' + str(sentiment) + ']</font>')
            overall_compound += float(sa['compound'])

        return review, status.HTTP_200_OK


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

        return jsonify(overall_compound = overall_compound, sentiments=results), status.HTTP_200_OK

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

        return jsonify(overall_compound = overall_compound, sentiments=results), status.HTTP_200_OK

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3008, threaded=True)
