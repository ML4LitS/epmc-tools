import click
import json
import requests
import os
from tqdm import tqdm
from ..jats_processor import XMLProcessor
from ..section_maps import ordered_labels
from ..api.articles import ArticlesClient

@click.group()
def local():
    """Commands for local file processing."""
    pass

@local.command()
@click.argument('input_path', type=click.STRING)
@click.argument('output_path', type=click.Path())
@click.option('--no-sentenciser', is_flag=True, default=False, help="Disable sentence splitting.")
def jats2json(input_path, output_path, no_sentenciser):
    """
    Converts a JATS XML file to JSON.

    The input can be a local file path, a URL, or a PMCID (e.g., PMC12345).
    The tool will automatically detect the input type.
    """
    processor = XMLProcessor(sentenciser=not no_sentenciser)
    xml_content = None

    try:
        if input_path.startswith('http://') or input_path.startswith('https://'):
            click.echo(f"Input identified as URL: {input_path}")
            response = requests.get(input_path)
            response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
            xml_content = response.text
        elif os.path.exists(input_path):
            click.echo(f"Input identified as local file: {input_path}")
            with open(input_path, 'r') as f:
                xml_content = f.read()
        elif input_path.upper().startswith('PMC'):
            click.echo(f"Input identified as PMCID: {input_path}")
            articles_client = ArticlesClient()
            xml_content = articles_client.get_fulltext_xml(input_path)
            if not xml_content:
                raise ValueError(f"Could not retrieve XML for PMCID {input_path}. It may not exist or may not have a full-text XML available.")
        else:
            raise FileNotFoundError(f"Input '{input_path}' is not a valid file path, URL, or PMCID.")

    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching content from URL: {e}", err=True)
        return
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        return
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        return
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        return

    if not xml_content:
        click.echo("Failed to retrieve any XML content.", err=True)
        return

    processed_data = processor.process_full_text(xml_content)
    final_json = processor.process_json(processed_data, ordered_labels)
    with open(output_path, 'w') as f:
        json.dump(final_json, f, indent=2)
    click.echo(f"Successfully converted {input_path} to {output_path}")

@local.command(name='extract-accessions-resources')
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('--offline', is_flag=True, default=False, help="Run in offline mode.")
def extract_accessions_resources(input_path, output_path, offline):
    """Extracts accession numbers and resources from a JSON file."""
    from ..spacy_extractor import extract_with_spacy
    import spacy
    nlp = spacy.load("en_core_sci_sm")
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    all_extractions = []
    total_sentences = sum(len(s) for s in data.get('sections', {}).values())

    # Set up three nested progress bars
    with tqdm(total=total_sentences, desc="Processing Sentences", position=0, leave=True) as sentence_pbar, \
         tqdm(desc="Accessions Found", position=1, unit=" acc", leave=True) as accession_pbar, \
         tqdm(desc="Resources Found ", position=2, unit=" res", leave=True) as resource_pbar:
        
        for section, sentences in data.get('sections', {}).items():
            for sentence in sentences:
                text = sentence.get('text', '')
                sentence_id = sentence.get('sentence_id')
                extraction_result = extract_with_spacy(nlp, text, section, sentence_id, offline=offline)
                
                if extraction_result:
                    for item in extraction_result:
                        if item['type'] == 'accession':
                            accession_pbar.update(1)
                        else:
                            resource_pbar.update(1)
                    all_extractions.extend(extraction_result)
                
                sentence_pbar.update(1)

    with open(output_path, 'w') as f:
        json.dump(all_extractions, f, indent=2)
    click.echo(f"\nSuccessfully extracted {len(all_extractions)} total items from {input_path} to {output_path}")
