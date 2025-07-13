
import argparse
import json
import requests
import gzip
import os
from .xml_processor import XMLProcessor, ordered_labels

def main():
    parser = argparse.ArgumentParser(description="A tool to extract structured JSON from JATS XML.")
    parser.add_argument("--input-file", help="Path to the local XML file to process.")
    parser.add_argument("--url", help="URL of the remote XML file to process.")
    parser.add_argument("--output-file", required=True, help="Path to save the output JSON file.")
    parser.add_argument("--no-sentences", action="store_true", help="Disable sentence splitting. Output paragraphs.")
    parser.add_argument("--accessions", action="store_true", help="Extract accession numbers and filter output to only include sentences/paragraphs with them.")

    args = parser.parse_args()

    if not args.input_file and not args.url:
        parser.error("Either --input-file or --url must be provided.")

    xml_content = ""
    try:
        if args.url:
            resp = requests.get(args.url, timeout=30)
            resp.raise_for_status()
            xml_content = resp.text
        else:
            if not os.path.exists(args.input_file):
                raise FileNotFoundError(f"Input file not found: {args.input_file}")
            open_func = gzip.open if args.input_file.endswith('.gz') else open
            with open_func(args.input_file, 'rt', encoding='utf8') as f:
                xml_content = f.read()
    except Exception as e:
        print(f"Error: {e}")
        return

    try:
        sentencise = not args.no_sentences
        if args.accessions:
            sentencise = True
        
        processor = XMLProcessor(sentenciser=sentencise, accessions=args.accessions)
        
        data_temp = processor.process_full_text(xml_content)
        if not data_temp:
            raise ValueError("Failed to extract data from the XML.")

        result = processor.process_json(data_temp, ordered_labels)

        with open(args.output_file, 'w', encoding='utf8') as f_out:
            json.dump(result, f_out, indent=2)
        
        print(f"Successfully processed and saved output to {args.output_file}")

    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
