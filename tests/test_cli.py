import subprocess
import json
import unittest
import xml.etree.ElementTree as ET

def run_command(command):
    """Runs a command and returns the output."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result

class TestEpmcCli(unittest.TestCase):

    def test_epmc_cli_search(self):
        """Tests the epmc-cli search command."""
        print("Testing epmc-cli (search)...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli articles search 'machine learning' --page-size 1"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("resultList", data)
        print("...PASSED")

    def test_epmc_cli_get(self):
        """Tests the epmc-cli get command."""
        print("Testing epmc-cli (get)...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli articles get PMC 11704132"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("result", data)
        self.assertEqual(data["result"]["pmcid"], "PMC11704132")
        print("...PASSED")

    def test_epmc_cli_references(self):
        """Tests the epmc-cli references command."""
        print("Testing epmc-cli (references)...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli articles references PMC 11704132"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("referenceList", data)
        print("...PASSED")

    def test_epmc_cli_fulltext(self):
        """Tests the epmc-cli fulltext command."""
        print("Testing epmc-cli (fulltext)...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli articles fulltext PMC11704132"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        # Check if the output is valid XML
        try:
            ET.fromstring(result.stdout)
        except ET.ParseError:
            self.fail("Output is not valid XML")
        print("...PASSED")

    def test_epmc_cli_grants_search(self):
        """Tests the epmc-cli grants search command."""
        print("Testing epmc-cli (grants search)...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli grants search 'cancer' --page-size 1"
        result = run_command(command)
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("RecordList", data)
        print("...PASSED")

if __name__ == '__main__':
    unittest.main()

