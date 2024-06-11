from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = 'AIzaSyD_nl2Hzfq3vebmDD5g1WUJ5OHNHe27tyc'

@app.route('/search', methods=['GET'])
def search_videos():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': YOUTUBE_API_KEY,
        'q': query,
        'part': 'snippet',
        'type': 'video',
        'maxResults': 10
    }
    response = requests.get(url, params=params)
    data = response.json()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
