.. _library_usage:

Using as a Library
==================

Beyond the command-line interface, you can import and use the core components of `europmc-dev-tool` directly in your Python scripts. This allows for greater flexibility and integration into your own custom workflows.

Key Components
--------------

*   **API Clients**: Located in `europmc_dev_tool.api`, these classes (`ArticlesClient`, `AnnotationsClient`, etc.) provide direct access to the Europe PMC APIs.
*   **JATS Processor**: The `XMLProcessor` class in `europmc_dev_tool.jats_processor` handles the conversion of JATS XML to structured JSON.
*   **Accession Number Extractor**: The `extract_with_spacy` function in `europmc_dev_tool.spacy_extractor` finds accession numbers in text.

Example Script
--------------

The following script, `script_usage_example.py`, demonstrates how to use these components to fetch an article from Europe PMC, process its XML, and extract accession numbers.

.. literalinclude:: ../script_usage_example.py
   :language: python
   :caption: script_usage_example.py

How to Run the Example
----------------------

1.  Ensure you have installed the package and its dependencies (see :doc:`installation`).
2.  Save the code above as `script_usage_example.py` in the root of the project directory.
3.  Run the script from your terminal:

    .. code-block:: bash

        python script_usage_example.py

The script will create two files, `example_output.json` and `example_accessions.json`, in your project directory.
