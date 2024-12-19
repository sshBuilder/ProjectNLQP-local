from flask import Flask, request, jsonify, render_template
from searchAgent import search_and_extract
from data_preprocessing import preprocess_data
from llama_api import query_llama_api
from utils import log_message

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Step 1: Fetch and extract data
        log_message("INFO", f"Received query: {user_query}")
        search_results = search_and_extract(user_query, num_results=10)
        log_message("INFO", "SearchAgent completed successfully.")

        # Step 2: Preprocess the data
        preprocessed_text = preprocess_data(search_results)
        log_message("INFO", f"Preprocessed text: {preprocessed_text}")

        # Step 3: Generate LLM response
        final_response = generate_llm_response(user_query, preprocessed_text)
        log_message("INFO", f"Llama API response: {final_response}")

        # Format and return the response
        formatted_response = format_response_as_html(final_response)
        return jsonify({"response": formatted_response})

    except Exception as e:
        log_message("ERROR", f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

from llama_api import query_llama_api

def generate_llm_response(query, preprocessed_information):
    """
    Generate a response using the LLM with a concise, educated prompt.
    Args:
        query (str): The user's query.
        preprocessed_information (str): The preprocessed information from search results.
    Returns:
        str: The LLM-generated response.
    """
    prompt = f"""
    Generate a well-educated response to the following query based on the provided information. 
    Use the details given to create a direct and factual answer without summarizing unnecessarily.

    Query: {query}

    Information:
    {preprocessed_information}

    Response:
    """
    return query_llama_api(prompt)


def format_response_as_html(response_text):
    """
    Format the LLM response as structured HTML for better frontend display.
    Args:
        response_text (str): Raw response from the LLM.
    Returns:
        str: HTML-formatted response.
    """
    # Split the response into sections using markdown-like conventions
    sections = response_text.split("**")
    formatted_sections = []

    for section in sections:
        if section.strip():
            if section.startswith("What") or section.startswith("Relationship") or section.startswith("Applications") or section.startswith("Key Characteristics"):
                formatted_sections.append(f"<h3>{section.strip()}</h3>")
            else:
                # Treat as a paragraph or list
                lines = section.strip().split("* ")
                for line in lines:
                    if line.strip():
                        if line.startswith("* "):
                            formatted_sections.append(f"<li>{line[1:].strip()}</li>")
                        else:
                            formatted_sections.append(f"<p>{line.strip()}</p>")

    # Wrap everything in a container div
    return "<div>" + "\n".join(formatted_sections) + "</div>"


@app.route('/')
def index():
    """
    Serve the home page.
    """
    return render_template('index.html')


if __name__ == "__main__":
    # Run the Flask server
    app.run(debug=True, port=5000)
