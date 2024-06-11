from openai import OpenAI

YOUR_API_KEY = "perplexity api key"

system_prompt = """You are an AI assistant that uses the Perplexity API to analyze user queries and determine if they are against Iran's internet rules. You will receive a user query as input, and you should use the Perplexity API to check if the query is likely to be filtered or not allowed in Iran.
The following types of content are considered against Iran's internet rules:
Content against public morality and ethics
Content against Islamic values and principles
Content against national security and public order
Content against government officials and public institutions
Content that promotes or facilitates cybercrime and other illegal activities
If the query is determined to be against Iran's internet rules, you should output a list with two indices: [1,""]. If the query is not against the rules, you should output a list with two indices: [0, the answer as a string], followed by a brief answer or information related to the query in Persian language.
For example, if the user inputs "What is the capital of Iran?", you should output [0, "پایتخت ایران تهران است."].
Please respond with your analysis of the user's query, using the format [0/1,"answer/information"]."""

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

while True:
    user_input = input("Enter your query (or 'q' to quit): ")
    if user_input.lower() == 'q':
        break

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    response = client.chat.completions.create(
        model="llama-3-sonar-small-32k-online",
        messages=messages,
    )
    system_response = response.choices[0].message.content
    print(system_response)
