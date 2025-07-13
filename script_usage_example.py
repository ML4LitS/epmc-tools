"""
Example script demonstrating how to use the europmc-dev-tool package
as a library in your own Python scripts.
"""

import json
import spacy
from europmc_dev_tool.api.articles import ArticlesClient
from europmc_dev_tool.jats_processor import XMLProcessor
from europmc_dev_tool.section_maps import ordered_labels
from europmc_dev_tool.spacy_extractor import extract_with_spacy

def run_api_examples():
    """Demonstrates how to use the API clients."""
    print("--- Running API Client Examples ---")
    
    # Instantiate the client. You can provide your email for better API etiquette.
    articles_client = ArticlesClient(email="your.email@example.com")

    # 1. Search for articles
    print("\n1. Searching for articles matching 'crispr'...")
    search_results = articles_client.search("crispr", page_size=5)
    print(f"Found {search_results.get('hitCount')} articles.")
    if search_results.get('resultList', {}).get('result'):
        first_article_id = search_results['resultList']['result'][0]['id']
        print(f"ID of the first article: {first_article_id}")

    # 2. Get metadata for a specific article
    print("\n2. Fetching metadata for article 'PMC11704132'...")
    article_data = articles_client.get_article(source="PMC", article_id="PMC11704132")
    print(f"Successfully fetched. Title: {article_data.get('result', {}).get('title')}")

    # 3. Get the full-text XML for an article
    print("\n3. Fetching full-text XML for article 'PMC11704132'...")
    full_text_xml = articles_client.get_fulltext_xml("PMC11704132")
    print("Full-text XML received (first 200 chars):")
    print(full_text_xml[:200] + "...")
    print("-" * 35)
    return full_text_xml


def run_local_processing_examples(xml_content):
    """Demonstrates JATS processing and accession number extraction."""
    print("\n--- Running Local Processing Examples ---")

    # 1. Convert JATS XML to structured JSON
    print("\n1. Processing JATS XML to JSON...")
    processor = XMLProcessor()
    processed_data = processor.process_full_text(xml_content)
    final_json = processor.process_json(processed_data, ordered_labels)
    
    # Save the intermediate JSON to a file (optional)
    with open("example_output.json", "w") as f:
        json.dump(final_json, f, indent=2)
    print("Processed JSON has been saved to 'example_output.json'")

    # 2. Extract accession numbers from the JSON content
    print("\n2. Extracting accession numbers...")
    
    # Load the required spaCy model
    try:
        nlp = spacy.load("en_core_sci_sm")
    except OSError:
        print("Error: 'en_core_sci_sm' model not found.")
        print("Please run: python -m spacy download en_core_sci_sm")
        return

    all_extractions = []
    # Iterate through the sections and sentences in your JSON structure
    for section, sentences in final_json.get('sections', {}).items():
        for sentence in sentences:
            text = sentence.get('text', '')
            # Call the extraction function
            extractions = extract_with_spacy(nlp, text, section)
            if extractions:
                all_extractions.extend(extractions)

    print(f"Found {len(all_extractions)} accession numbers.")
    if all_extractions:
        print("Example of extracted data:")
        print(json.dumps(all_extractions[0], indent=2))

    # Save the extractions to a file (optional)
    with open("example_accessions.json", "w") as f:
        json.dump(all_extractions, f, indent=2)
    print("Extracted accession numbers saved to 'example_accessions.json'")
    print("-" * 35)


if __name__ == "__main__":
    # Run the API examples and get the XML content
    xml_from_api = run_api_examples()

    # Use the fetched XML to run the local processing examples
    if xml_from_api:
        run_local_processing_examples(xml_from_api)

    # You can also process a local file directly
    # print("\n--- Processing a local XML file ---")
    # with open("test_data/PXD053361.xml", "r") as f:
    #     local_xml_content = f.read()
    # run_local_processing_examples(local_xml_content)

