from flask import Flask, request, jsonify, send_from_directory , render_template

import requests
from openai import OpenAI
import json
import logging
import credentials
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__, static_folder='static', static_url_path='')

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# YouTube API key
YOUTUBE_API_KEY = credentials.yotube_api_key

# Perplexity AI API key
PERPLEXITY_API_KEY = credentials.perplexity_api_key

system_prompt = """You are an AI assistant that uses the Perplexity API to analyze user queries and determine if they are against Iran's internet rules. You will receive a user query as input, and you should use the Perplexity API to check if the query is likely to be filtered or not allowed in Iran.
The following types of content are considered against Iran's internet rules:
Content against public morality and ethics
Content against Islamic values and principles
Content against national security and public order
Content against government officials and public institutions
Content that promotes or facilitates cybercrime and other illegal activities
If the query is determined to be against Iran's internet rules, you should output a list with two indices: [1,[""]]. If the query is not against the rules, you should output a list with two indices: [[0], [the answer as a string]], followed by a brief answer or information related to the query in Persian language.
For example, if the user inputs "What is the capital of Iran?", you should output [0, ["پایتخت ایران تهران است."]].
Please respond with your analysis of the user's query, using the format [0/1,["answer/information"]]."""

client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

@app.route('/')
def index():
    return send_from_directory('static', 'Frame60-dark.html')

# @app.route('/search', methods=['GET'])
# def search_videos():
#     query = request.args.get('q')
#     if not query:
#         return jsonify({'error': 'Missing query parameter'}), 400

#     # Perplexity AI analysis
#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": query},
#     ]

#     perplexity_response = client.chat.completions.create(
#         model="llama-3-sonar-small-32k-online",
#         messages=messages,
#     )
#     analysis_result = perplexity_response.choices[0].message.content

#     # Log the Perplexity API response for debugging
#     logging.debug(f'Perplexity API response: {analysis_result}')

#     # Check if the content is filtered
#     try:
#         analysis_data = json.loads(analysis_result)
#     except json.JSONDecodeError as e:
#         logging.error(f'Failed to parse Perplexity API response: {e}')
#         return jsonify({'error': 'Failed to parse Perplexity API response', 'details': str(e)}), 500

#     if analysis_data[0] == 1:
#         return jsonify({'filtered': True, 'message': 'Content is filtered and cannot be displayed.'})

#     # YouTube API search
#     url = 'https://www.googleapis.com/youtube/v3/search'
#     params = {
#         'key': YOUTUBE_API_KEY,
#         'q': query,
#         'part': 'snippet',
#         'type': 'video',
#         'maxResults': 12
#     }

#     response = requests.get(url, params=params)
#     data = response.json()
    
#     #/////////////////////////////////////
#     test_message="مهراد هیدن یک خواننده رپ و هیپ هاپ ایرانی است که در سبک رپ و راک و هیپ هاپ فعالیت می‌کند. او در سال ۱۳۶۳ در تهران متولد شد و در سال ۱۳۸۱ فعالیت هنری خود را آغاز کرد. او به همراه گروه زدبازی و دیگر هنرمندان همکاری داشته و آلبوم‌های مختلفی منتشر کرده است. مهراد هیدن در بین طرفداران رپ فارسی بسیار محبوب است و کنسرت‌های بسیاری برگزار کرده است."
#     # Combine results
#     result = {
#         'filtered': False,
#         'ai_message': test_message,
#         'videos': data['items']
#     }

#     return jsonify(result)

@app.route('/video/<video_id>')
def video(video_id):
    return render_template('video_player.html', video_id=video_id)

def fetch_piped_thumbnail(video_id):
    piped_api_url = f'https://pipedapi.kavin.rocks/streams/{video_id}'
    response = requests.get(piped_api_url)
    if response.status_code == 200:
        data = response.json()
        return video_id, data['thumbnailUrl'], data["uploaderAvatar"]
    else:
        logging.error(f"Failed to fetch thumbnail for video {video_id} from Piped API")
        return video_id, None

@app.route('/search_list/<query>')
    
def search_videos(query):
    
    
    print(query)
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    # Perplexity AI analysis
    # messages = [
    #     {"role": "system", "content": system_prompt},
    #     {"role": "user", "content": query},
    # ]

    # perplexity_response = client.chat.completions.create(
    #     model="llama-3-sonar-small-32k-online",
    #     messages=messages,
    # )
    # analysis_result = perplexity_response.choices[0].message.content

    # # Log the Perplexity API response for debugging
    # logging.debug(f'Perplexity API response: {analysis_result}')

    # # Check if the content is filtered
    # try:
    #     analysis_data = json.loads(analysis_result)
    # except json.JSONDecodeError as e:
    #     logging.error(f'Failed to parse Perplexity API response: {e}')
    #     return jsonify({'error': 'Failed to parse Perplexity API response', 'details': str(e)}), 500

    # if analysis_data[0] == 1:
    #     return jsonify({'filtered': True, 'message': 'Content is filtered and cannot be displayed.'})

    # YouTube API search
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': YOUTUBE_API_KEY,
        'q': query,
        'part': 'snippet',
        'type': 'video',
        'maxResults': 12
    }

    response = requests.get(url, params=params)
    data = response.json()

    #replace thumbnail with piped api ( it is filter in iran)
    
     # Fetch Piped API thumbnails in parallel
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_video = {executor.submit(fetch_piped_thumbnail, video['id']['videoId']): video for video in data['items']}

        for future in as_completed(future_to_video):
            video = future_to_video[future]
            try:
                video_id, thumbnail_url ,uploader_avatar= future.result()
                if thumbnail_url:
                    video['snippet']['thumbnails']['default']['url'] = thumbnail_url
                    video['snippet']['thumbnails']['medium']['url'] = thumbnail_url
                    video['snippet']['thumbnails']['high']['url'] = thumbnail_url
                if uploader_avatar:
                    video['snippet']['uploader_avatar'] = uploader_avatar
                    

            except Exception as exc:
                logging.error(f"Generated an exception: {exc}")

    
    test_message = "مهراد هیدن یک خواننده رپ و هیپ هاپ ایرانی است که در سبک رپ و راک و هیپ هاپ فعالیت می‌کند. او در سال ۱۳۶۳ در تهران متولد شد و در سال ۱۳۸۱ فعالیت هنری خود را آغاز کرد. او به همراه گروه زدبازی و دیگر هنرمندان همکاری داشته و آلبوم‌های مختلفی منتشر کرده است. مهراد هیدن در بین طرفداران رپ فارسی بسیار محبوب است و کنسرت‌های بسیاری برگزار کرده است."
    
    result = {
        'filtered': False,
        'ai_message': test_message,
        'videos': data['items'],
        'query': query
    }

    return render_template('results.html', result=json.dumps(result))
if __name__ == '__main__':  
    app.run(debug=True)

