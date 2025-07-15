# Europe PMC Development Tool

`epmc-tools` is a Python package that provides a powerful command-line interface (`epmc-cli`) and library for interacting with scientific literature. It allows you to:

*   Process JATS XML from local files or URLs, converting them to JSON.
*   Extract accession numbers from text.
*   Split text into sentences.
*   Access the Europe PMC APIs for searching articles, grants, and annotations.
*   Harvest metadata via the OAI-PMH service.

## Installation

To install the package, clone the repository and install it using pip:

```bash
git clone https://github.com/ML4LitS/epmc-tools.git
cd epmc-tools
pip install .
```

### Dependencies

The required Python packages will be installed automatically. However, the tool also relies on `scispacy` model, which needs to be downloaded separately.

```bash
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz
```

### Editable Mode

If you are developing the package, you may want to install it in editable mode:

```bash
pip install -e .
```

## Usage

The tool can be used as a command-line interface (`epmc-cli`) or as a Python library.

### Command-Line Interface

The `epmc-cli` tool provides a command-line interface for the Europe PMC API and for local file processing.

#### Local Commands

The `local` commands process files on your machine or from the web.

*   **Convert JATS XML to JSON:**
    The `jats2json` command can intelligently handle a local file path, a URL, or a PMCID.

    *From a local file:*
    ```bash
    epmc-cli local jats2json test_data/PXD053361.xml output.json
    ```
    *From a PMCID:*
    ```bash
    epmc-cli local jats2json PMC11704132 output.json
    ```
    *From a URL (with sentence splitting disabled):*
    ```bash
    epmc-cli local jats2json https://some-url/article.xml output.json --no-sentenciser
    ```

*   **Extract accession numbers:**
    This command processes the JSON file created by `jats2json`.
    ```bash
    epmc-cli local extract-accessions-resources output.json accessions.json
    ```

#### API Commands

*   **Search for articles:**
    ```bash
    epmc-cli articles search "BRCA1" --page-size 1
    ```
*   **Get article metadata:**
    ```bash
    epmc-cli articles get PMC11704132
    ```
*   **Get full-text XML:**
    ```bash
    epmc-cli articles fulltext PMC11704132
    ```

For more detailed usage instructions, please refer to the [documentation](https://epmc-tools.readthedocs.io/en/latest/).

### Library

The core components of `europmc-dev-tool` can be imported and used directly in your Python scripts. This allows for greater flexibility and integration into your own custom workflows.

A full example can be found in `script_usage_example.py`, which shows how to build a robust pipeline. Here is a simplified version:

```python
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
    """
    if identifier.startswith('http'):
        response = requests.get(identifier)
        response.raise_for_status()
        return response.text
    elif os.path.exists(identifier):
        with open(identifier, 'r') as f:
            return f.read()
    elif identifier.upper().startswith('PMC'):
        articles_client = ArticlesClient()
        return articles_client.get_fulltext_xml(identifier)
    else:
        raise ValueError("Input is not a valid file path, URL, or PMCID.")

# 1. Fetch content (example with a PMCID)
xml_content = get_xml_content("PMC11704132")

if xml_content:
    # 2. Process the JATS XML to JSON
    processor = XMLProcessor()
    processed_data = processor.process_full_text(xml_content)
    final_json = processor.process_json(processed_data, ordered_labels)

    # 3. Extract accession numbers and resources
    nlp = spacy.load("en_core_sci_sm")
    all_extractions = []
    for section, sentences in final_json.get('sections', {}).items():
        for sentence in sentences:
            text = sentence.get('text', '')
            sentence_id = sentence.get('sentence_id')
            extractions = extract_with_spacy(nlp, text, section, sentence_id)
            if extractions:
                all_extractions.extend(extractions)

    print(json.dumps(all_extractions, indent=2))
```

For more detailed usage instructions, please refer to the [documentation](https://epmc-tools.readthedocs.io/en/latest/).
