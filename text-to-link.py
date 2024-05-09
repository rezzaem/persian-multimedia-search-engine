from openai import OpenAI
import requests
from bs4 import BeautifulSoup

YOUR_API_KEY = "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"

def fetch_search_results(query):
    search_engine_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    response = requests.get(search_engine_url)
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("div", class_="g")

    links = []
    for result in search_results:
        link = result.find("a")
        if link:
            links.append(link["href"])

    return links

def get_related_videos(query):
    messages = [
        {"role": "system", "content": "You are an artificial intelligence assistant and you need to engage in a helpful, detailed, polite conversation with a user."},
        {"role": "user", "content": f"I'm looking for videos related to '{query}'. Can you provide some relevant video links or descriptions?"}
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # Chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
    )
    print(response)

    # Chat completion with streaming
    response_stream = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
        stream=True,
    )
    for response in response_stream:
        print(response)

    related_videos = response.choices[0].message.content
    return related_videos

user_query = input("Enter your query: ")

# Get related videos from Perplexity API
related_videos = get_related_videos(user_query)
print("Related videos from Perplexity API:")
print(related_videos)

# Get search results from Google
search_results = fetch_search_results(user_query)
print("\nSearch results from Google:")
for link in search_results:
    print(link)