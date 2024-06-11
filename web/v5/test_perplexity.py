import openai
import credentials
# Perplexity AI API key
PERPLEXITY_API_KEY = credentials.perplexity_api_key

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

# Initialize OpenAI client with API key
openai.api_key = PERPLEXITY_API_KEY

def analyze_query(query):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="llama-3-sonar-small-32k-online",
            messages=messages,
        )
        analysis_result = response.choices[0].message['content']
        return analysis_result
    except openai.APIStatusError as e:
        print("Authentication failed. Please check the API key.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    user_input = "What is the capital of Iran?"
    result = analyze_query(user_input)
    print(result)
