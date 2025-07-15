"""
Example script demonstrating how to use the europmc-dev-tool package
as a library in your own Python scripts.
"""

import json
import os
import requests
import spacy
from europmc_dev_tool.api.articles import ArticlesClient
from europmc_dev_tool.jats_processor import XMLProcessor
from europmc_dev_tool.section_maps import ordered_labels
from europmc_dev_tool.spacy_extractor import extract_with_spacy


def get_xml_content(identifier):
    """
    Intelligently fetches JATS XML content from a PMCID, URL, or local file.

    :param identifier: A PMCID (e.g., "PMC12345"), a URL, or a local file path.
    :type identifier: str
    :return: The XML content as a string, or None if fetching fails.
    :rtype: str or None
    """
    xml_content = None
    try:
        if identifier.startswith('http://') or identifier.startswith('https://'):
            print(f"Identifier recognized as URL: {identifier}")
            response = requests.get(identifier)
            response.raise_for_status()  # Raises HTTPError for bad responses
            xml_content = response.text
        elif os.path.exists(identifier):
            print(f"Identifier recognized as local file: {identifier}")
            with open(identifier, 'r') as f:
                xml_content = f.read()
        elif identifier.upper().startswith('PMC'):
            print(f"Identifier recognized as PMCID: {identifier}")
            articles_client = ArticlesClient()
            xml_content = articles_client.get_fulltext_xml(identifier)
            if not xml_content:
                raise ValueError(f"Could not retrieve XML for PMCID {identifier}.")
        else:
            raise FileNotFoundError(f"Identifier '{identifier}' is not a valid file path, URL, or PMCID.")
    except (requests.exceptions.RequestException, FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return None
    
    print("Successfully fetched XML content.")
    return xml_content


def run_processing_pipeline(xml_content, offline=False):
    """Demonstrates JATS processing and accession number extraction."""
    print("\n--- Running Local Processing Examples ---")

    # 1. Convert JATS XML to structured JSON
    print("\n1. Processing JATS XML to JSON...")
    processor = XMLProcessor()
    processed_data = processor.process_full_text(xml_content)
    final_json = processor.process_json(processed_data, ordered_labels)
    
    if not final_json:
        print("Processing failed to produce JSON. Aborting.")
        return

    # Save the intermediate JSON to a file (optional)
    with open("example_output.json", "w") as f:
        json.dump(final_json, f, indent=2)
    print("Processed JSON has been saved to 'example_output.json'")

    # 2. Extract accession numbers and resources from the JSON content
    print("\n2. Extracting accession numbers and resources...")
    
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
            sentence_id = sentence.get('sentence_id')
            # Call the extraction function
            extractions = extract_with_spacy(nlp, text, section, sentence_id, offline=offline)
            if extractions:
                all_extractions.extend(extractions)

    print(f"Found {len(all_extractions)} accession numbers and resources.")
    if all_extractions:
        print("Example of extracted data:")
        print(json.dumps(all_extractions[0], indent=2))

    # Save the extractions to a file (optional)
    with open("example_accessions.json", "w") as f:
        json.dump(all_extractions, f, indent=2)
    print("Extracted accession numbers and resources saved to 'example_accessions.json'")
    print("-" * 35)


if __name__ == "__main__":
    # --- Example with a PMCID ---
    print("--- Running example with PMCID: PMC11704132 ---")
    pmcid_content = get_xml_content("PMC11704132")
    if pmcid_content:
        run_processing_pipeline(pmcid_content)

    # --- Example with a local file ---
    # Note: Assumes 'test_data/PXD053361.xml' exists.
    print("\n--- Running example with local file: test_data/PXD053361.xml ---")
    local_file_content = get_xml_content("test_data/PXD053361.xml")
    if local_file_content:
        run_processing_pipeline(local_file_content)
        
    # --- Example with a URL ---
    # print("\n--- Running example with URL ---")
    # url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11704132/fullTextXML"
    # url_content = get_xml_content(url)
    # if url_content:
    #     run_processing_pipeline(url_content)

