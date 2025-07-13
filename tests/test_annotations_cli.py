import subprocess
import json
import unittest

def run_command(command):
    """Runs a command and returns the output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=60)
        return result
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {command}")
        return None

class TestAnnotationsCli(unittest.TestCase):

    def test_annotations_by_id(self):
        """Tests getting annotations by article ID."""
        print("Testing annotations by-id...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli annotations by-id PMC:11704132"
        result = run_command(command)
        self.assertIsNotNone(result)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["pmcid"], "PMC11704132")
        print("...PASSED")

    def test_annotations_by_entity(self):
        """Tests finding articles by entity."""
        print("Testing annotations by-entity...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli annotations by-entity p53"
        result = run_command(command)
        self.assertIsNotNone(result)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("articles", data)
        self.assertIsInstance(data["articles"], list)
        print("...PASSED")

    def test_annotations_by_type_accession(self):
        """Tests getting data accession annotations."""
        print("Testing annotations by-type (data accession)...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli annotations by-type --type 'Accession Numbers' --subtype 'uniprot'"
        result = run_command(command)
        self.assertIsNotNone(result)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("articles", data)
        self.assertIsInstance(data["articles"], list)
        print("...PASSED")

    def test_annotations_by_type_gene(self):
        """Tests getting gene annotations."""
        print("Testing annotations by-type (gene)...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli annotations by-type --type 'Gene_Proteins'"
        result = run_command(command)
        self.assertIsNotNone(result)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("articles", data)
        self.assertIsInstance(data["articles"], list)
        print("...PASSED")

if __name__ == '__main__':
    unittest.main()
