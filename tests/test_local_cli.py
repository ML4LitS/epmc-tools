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

    def tearDown(self):
        if os.path.exists(self.output_json):
            os.remove(self.output_json)
        if os.path.exists(self.accession_json):
            os.remove(self.accession_json)

    def test_jats2json(self):
        """Tests the jats2json command."""
        print("Testing jats2json...")
        command = f"/home/stirunag/environments/envs/env-epmc-tools/bin/python -m europmc_dev_tool.cli local jats2json {self.input_xml} {self.output_json}"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.output_json))
        with open(self.output_json, 'r') as f:
            data = json.load(f)
        self.assertIn('sections', data)
        print("...PASSED")

    def test_extract_accessions_resources_content(self):
        """Tests the extract-accessions-resources command and validates its content."""
        print("Testing extract-accessions-resources content...")
        # 1. Create a known input file for the extractor
        jats2json_command = f"/home/stirunag/environments/envs/env-epmc-tools/bin/python -m europmc_dev_tool.cli local jats2json {self.input_xml} {self.output_json}"
        run_command(jats2json_command)
        self.assertTrue(os.path.exists(self.output_json))

        # 2. Run the extractor command
        command = f"/home/stirunag/environments/envs/env-epmc-tools/bin/python -m europmc_dev_tool.cli local extract-accessions-resources {self.output_json} {self.accession_json}"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.accession_json))

        # 3. Validate the output content
        with open(self.accession_json, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        # Check if at least one expected accession number is found
        found = any(item.get('exact') == 'Q9H6L5' for item in data)
        self.assertTrue(found, "Expected accession number 'Q9H6L5' not found in the output.")
        print("...PASSED")

    def test_jats2json_url(self):
        """Tests the jats2json command with a URL."""
        print("Testing jats2json with URL...")
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11704132/fullTextXML"
        command = f"/home/stirunag/environments/envs/env-epmc-tools/bin/python -m europmc_dev_tool.cli local jats2json {url} {self.output_json}"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.output_json))
        with open(self.output_json, 'r') as f:
            data = json.load(f)
        self.assertIn('sections', data)
        print("...PASSED")

if __name__ == '__main__':
    unittest.main()
