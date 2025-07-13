import click
import json
import requests
from ..jats_processor import XMLProcessor
from ..section_maps import ordered_labels

@click.group()
def local():
    """Commands for local file processing."""
    pass

@local.command()
@click.argument('input_path', type=click.STRING)
@click.argument('output_path', type=click.Path())
@click.option('--no-sentenciser', is_flag=True, default=False, help="Disable sentence splitting.")
def jats2json(input_path, output_path, no_sentenciser):
    """Converts a JATS XML file from a local path or URL to JSON."""
    processor = XMLProcessor(sentenciser=not no_sentenciser)
    if input_path.startswith('http://') or input_path.startswith('https://'):
        response = requests.get(input_path)
        response.raise_for_status()
        xml_content = response.text
    else:
        with open(input_path, 'r') as f:
            xml_content = f.read()
    processed_data = processor.process_full_text(xml_content)
    final_json = processor.process_json(processed_data, ordered_labels)
    with open(output_path, 'w') as f:
        json.dump(final_json, f, indent=2)
    click.echo(f"Successfully converted {input_path} to {output_path}")

@local.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def extract_accessions(input_path, output_path):
    """Extracts accession numbers from a JSON file."""
    from ..spacy_extractor import extract_with_spacy
    import spacy
    nlp = spacy.load("en_core_sci_sm")
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    all_extractions = []
    for section, sentences in data.get('sections', {}).items():
        for sentence in sentences:
            text = sentence.get('text', '')
            extractions = extract_with_spacy(nlp, text, section)
            all_extractions.extend(extractions)

    with open(output_path, 'w') as f:
        json.dump(all_extractions, f, indent=2)
    click.echo(f"Successfully extracted accession numbers from {input_path} to {output_path}")
