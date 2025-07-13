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

*   **Convert JATS XML to JSON (with sentence splitting by default):**
    ```bash
    epmc-cli local jats2json test_data/PXD053361.xml output.json
    ```
*   **Convert JATS XML to JSON (without sentence splitting):**
    ```bash
    epmc-cli local jats2json test_data/PXD053361.xml output.json --no-sentenciser
    ```
*   **Extract accession numbers:**
    ```bash
    epmc-cli local extract-accessions output.json accessions.json
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

```python
import json
import spacy
from europmc_dev_tool.api.articles import ArticlesClient
from europmc_dev_tool.jats_processor import XMLProcessor
from europmc_dev_tool.section_maps import ordered_labels
from europmc_dev_tool.spacy_extractor import extract_with_spacy

# 1. Fetch an article from Europe PMC
articles_client = ArticlesClient(email="your.email@example.com")
full_text_xml = articles_client.get_fulltext_xml("PMC11704132")

# 2. Process the JATS XML to JSON
processor = XMLProcessor()
processed_data = processor.process_full_text(full_text_xml)
final_json = processor.process_json(processed_data, ordered_labels)

# 3. Extract accession numbers
nlp = spacy.load("en_core_sci_sm")
all_extractions = []
for section, sentences in final_json.get('sections', {}).items():
    for sentence in sentences:
        text = sentence.get('text', '')
        extractions = extract_with_spacy(nlp, text, section)
        if extractions:
            all_extractions.extend(extractions)

print(json.dumps(all_extractions, indent=2))
```

For more detailed usage instructions, please refer to the [documentation](https://epmc-tools.readthedocs.io/en/latest/).
