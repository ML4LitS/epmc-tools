import subprocess
import xml.etree.ElementTree as ET
import unittest

def run_command(command):
    """Runs a command and returns the output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=60)
        return result
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {command}")
        return None

class TestOaiCli(unittest.TestCase):

    def test_oai_harvest(self):
        """Tests the oai harvest command."""
        print("Testing oai harvest...")
        command = "/home/stirunag/environments/envs/env_jats2json/bin/python -m europmc_dev_tool.cli oai harvest --metadata-prefix oai_dc"
        result = run_command(command)
        self.assertIsNotNone(result)
        self.assertEqual(result.returncode, 0)
        # Check if the output is valid XML
        try:
            ET.fromstring(result.stdout)
        except ET.ParseError:
            self.fail("Output is not valid XML")
        print("...PASSED")

if __name__ == '__main__':
    unittest.main()

