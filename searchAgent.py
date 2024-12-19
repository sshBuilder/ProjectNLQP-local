import requests
import random
from bs4 import BeautifulSoup
import json

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0'
]

def perform_google_search(query, num_results=10):
    """
    Perform a Google search for the given query and retrieve top URLs.
    """
    try:
        # Load API credentials
        with open("config/API_KEY") as f:
            API_KEY = f.read().strip()
        with open("config/SEARCH_ID") as f:
            SEARCH_ID = f.read().strip()

        url = "https://www.googleapis.com/customsearch/v1"
        search_params = {
            "key": API_KEY,
            "cx": SEARCH_ID,
            "q": query,
            "num": num_results
        }

        response = requests.get(url, params=search_params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        result = response.json()

        # Extract URLs from search results
        if 'items' in result:
            return [item['link'] for item in result['items']]
        return []

    except Exception as e:
        print(f"Error performing Google search: {e}")
        return []


def fetch_content(url):
    """
    Fetch the content of a webpage.
    """
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_info(content, url):
    """
    Extract useful information from webpage content.
    """
    try:
        soup = BeautifulSoup(content, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]
        return {"url": url, "title": title, "content": paragraphs}
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return {"url": url, "title": "Error", "content": []}


def search_and_extract(query, num_results=10):
    """
    Perform a Google search and extract information from the top results.
    Args:
        query (str): The search query.
        num_results (int): Number of results to fetch.
    Returns:
        list: A list of dictionaries containing URL, title, and content.
    """
    print(f"Searching for: {query}")
    urls = perform_google_search(query, num_results)
    if not urls:
        print("No URLs retrieved from Google search.")
        return []

    results = []
    for url in urls:
        print(f"Processing URL: {url}")
        content = fetch_content(url)
        if content:
            extracted_info = extract_info(content, url)
            results.append(extracted_info)
            print(f"Data extracted for URL: {url}")

    return results


if __name__ == "__main__":
    # Example query for testing
    search_query = "What is the last date to file ITR in India?"
    results = search_and_extract(search_query)
    print(json.dumps(results, indent=4, ensure_ascii=False))
