import warnings
warnings.filterwarnings("ignore")

import json
from flask import Flask, render_template, Response, request

from preprocessing import query_processing
from preprocessing import load_articles




app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def search():

    query = request.form['query']

    sims = query_processing(query)

    articles = load_articles()

    top_articles = [articles[sim[0]] for sim in sims[:10]]

    return render_template('result.html', articles=top_articles)


if __name__ == '__main__':
    
    #  Production
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

    # local run
    # app.run(debug=True,port=5000)
