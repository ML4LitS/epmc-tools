import unittest
import subprocess
import os
import json

def run_command(command):
    """Runs a command and returns the output."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result

class TestLocalCli(unittest.TestCase):

    def setUp(self):
        self.input_xml = 'test_data/PXD053361.xml'
        self.output_json = 'test_output.json'
        self.accession_json = 'accession_extraction_output.json'
        run_command("/home/stirunag/environments/envs/env_jats2json/bin/python -m spacy download en_core_sci_sm")

    def tearDown(self):
        if os.path.exists(self.output_json):
            os.remove(self.output_json)
        if os.path.exists(self.accession_json):
            os.remove(self.accession_json)

    def test_jats2json(self):
        """Tests the jats2json command."""
        print("Testing jats2json...")
        command = f"/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli local jats2json {self.input_xml} {self.output_json}"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.output_json))
        with open(self.output_json, 'r') as f:
            data = json.load(f)
        self.assertIn('sections', data)
        print("...PASSED")

    def test_extract_accessions(self):
        """Tests the extract-accessions command."""
        print("Testing extract-accessions...")
        # First, create the JSON file
        jats2json_command = f"/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli local jats2json {self.input_xml} {self.output_json}"
        run_command(jats2json_command)
        
        command = f"/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli local extract-accessions {self.output_json} {self.accession_json}"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.accession_json))
        with open(self.accession_json, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        print("...PASSED")

    def test_jats2json_url(self):
        """Tests the jats2json command with a URL."""
        print("Testing jats2json with URL...")
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11704132/fullTextXML"
        command = f"/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli local jats2json {url} {self.output_json}"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.output_json))
        with open(self.output_json, 'r') as f:
            data = json.load(f)
        self.assertIn('sections', data)
        print("...PASSED")

if __name__ == '__main__':
    unittest.main()
