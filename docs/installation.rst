============
Installation
============

To install the package, clone the repository and install it using pip:

.. code-block:: bash

   git clone https://github.com/ML4LitS/epmc-tools.git
   cd epmc-tools
   pip install .

Dependencies
------------

The required Python packages will be installed automatically. However, the tool also relies on a `spacy` model, which needs to be downloaded separately.

.. code-block:: bash

   pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz

Editable Mode
-------------

If you are developing the package, you may want to install it in editable mode from the root of the project directory:

.. code-block:: bash

   pip install -e .
