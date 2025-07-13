import unittest
from unittest.mock import patch, MagicMock
from .epmcapi import EPMCClient

class TestEPMCClient(unittest.TestCase):

    def test_client_initialization(self):
        """Test that the EPMCClient can be initialized."""
        client = EPMCClient(email="test@example.com", tool="test_tool")
        self.assertIsNotNone(client)

    @patch('requests.Session.get')
    def test_search_articles_success(self, mock_get):
        """Test a successful search_articles call."""
        # Configure the mock to return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resultList": {"result": [{"id": "123"}]}}
        mock_get.return_value = mock_response

        # Initialize the client and make the call
        client = EPMCClient(email="test@example.com", tool="test_tool")
        result = client.search_articles("test query")

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["resultList"]["result"][0]["id"], "123")
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
