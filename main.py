import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS

from SitemapFeed import SitemapFeed
from WaymoreParser import WaymoreParser

app = Flask(__name__)
load_dotenv('config.env')
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'OK!'})


@app.route('/sitemap', methods=['GET'])
def sitemap_feed():
    url = request.args.get('url')
    sf = SitemapFeed()
    fp = sf.process(url)
    return jsonify({'RESULT:': fp})


@app.route('/waymore', methods=['POST'])
def waymore_parse():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Empty file name'}), 400

    filepath = os.path.join(os.environ.get("UPLOAD_FOLDER"), file.filename)
    file.save(filepath)

    wp = WaymoreParser()
    result = wp.process(filepath)

    return jsonify({'message': f'Files uploaded: {result}'}), 200


if __name__ == '__main__':
    app.run(port=4444)
