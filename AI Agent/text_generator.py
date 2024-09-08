import openai
from elasticsearch_helper import retrieve_relevant_docs
from elasticsearch.exceptions import ElasticsearchException

# OpenAI GPT-4 initialization (replace with your actual key)
openai.api_key = 'your-openai-api-key'

# Helper function to generate text from OpenAI GPT-4
def generate_text(prompt):
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None
        )
        # Ensure response is not empty
        if response and response.choices:
            return response.choices[0].text.strip()
        else:
            return "No content generated."
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "An error occurred during text generation."

# Main function to generate creative content
def generate_creative_content(query):
    try:
        # Retrieve relevant documents using BM25 from Elasticsearch
        relevant_docs = retrieve_relevant_docs(query)
        
        # Check if any relevant documents were retrieved
        if not relevant_docs:
            return "No relevant documents found for the query."

        # Create a more contextually relevant prompt based on retrieved documents
        full_prompt = (
            f"Based on the following documents:\n\n{relevant_docs}\n\n"
            f"Generate a creative blog post, script, or social media caption for the topic: '{query}'."
        )

        # Generate creative content using GPT-4
        return generate_text(full_prompt)
    except ElasticsearchException as es_err:
        print(f"Elasticsearch error: {es_err}")
        return "An error occurred while retrieving relevant documents from Elasticsearch."
    except Exception as e:
        print(f"General error: {e}")
        return "An error occurred during content generation."

# Example usage
if __name__ == "__main__":
    query = "How to improve productivity"
    content = generate_creative_content(query)
    print(content)
