from .client import BaseClient

class GrantsClient(BaseClient):
    """
    Client for the Europe PMC Grants RESTful API.
    """
    BASE_URL = "https://www.ebi.ac.uk/europepmc/GristAPI/rest/get/"

    def search(self, query: str, page: int = 1, page_size: int = 25) -> dict:
        """Search grants via /search endpoint."""
        url = f"{self.BASE_URL}query={query}&format=json&page={page}&pageSize={page_size}"
        return self._get(url)

