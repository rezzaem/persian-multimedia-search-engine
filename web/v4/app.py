from flask import Flask, request, jsonify
from  openai import OpenAI

app = Flask(__name__)

YOUR_API_KEY = "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"
system_prompt = """You are an AI assistant that uses the Perplexity API to analyze user queries and determine if they are against Iran's internet rules. You will receive a user query as input, and you should use the Perplexity API to check if the query is likely to be filtered or not allowed in Iran. The following types of content are considered against Iran's internet rules: \* Content against public morality and ethics \* Content against Islamic values and principles \* Content against national security and public order \* Content against government officials and public institutions \* Content that promotes or facilitates cybercrime and other illegal activities If the query is determined to be against Iran's internet rules, you should output "filtered". If the query is not against the rules, you should output "ok". Please respond with your analysis of the user's query, using the format "filtered" or "ok"."""

messages = [{"role": "system", "content": system_prompt}]
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="llama-3-sonar-small-32k-online",
        messages=messages,
    )
    result = response.choices[0].message.content
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)