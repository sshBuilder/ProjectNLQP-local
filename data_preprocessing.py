def preprocess_data(json_data):
    """
    Extract and preprocess data from JSON for use in the LLM prompt.
    Args:
        json_data (list): Parsed JSON data from search results.
    Returns:
        str: Concatenated relevant content for the LLM prompt.
    """
    relevant_texts = []
    for entry in json_data:
        # Extract the title and the first paragraph for each result
        title = entry.get("title", "No Title")
        content = entry.get("content", [])
        if content:
            # Take only the first paragraph as the most relevant
            relevant_texts.append(f"{title}: {content[0]}")

    # Join all relevant texts with line breaks
    return "\n".join(relevant_texts)
