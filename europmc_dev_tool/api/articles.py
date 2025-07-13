from .client import BaseClient

class ArticlesClient(BaseClient):
    """
    Client for the Europe PMC Articles RESTful API.
    """
    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"

    def search(self, query: str, page: int = 1, page_size: int = 25, result_type: str = "core") -> dict:
        """Search articles via /search endpoint."""
        url = f"{self.BASE_URL}/search"
        params = self._build_params({
            "query": query,
            "page": page,
            "pageSize": page_size,
            "resultType": result_type
        })
        return self._get(url, params)

    def get_article(self, source: str, article_id: str, result_type: str = "core") -> dict:
        """Fetch metadata for a single article by ID."""
        url = f"{self.BASE_URL}/article/{source}/{article_id}"
        params = self._build_params({
            "resultType": result_type
        })
        return self._get(url, params)

    def get_references(self, source: str, article_id: str, page: int = 1, page_size: int = 25) -> dict:
        """Fetch references for a single article by ID."""
        url = f"{self.BASE_URL}/{source}/{article_id}/references"
        params = self._build_params({
            "page": page,
            "pageSize": page_size
        })
        return self._get(url, params)

    def get_fulltext_xml(self, article_id: str) -> str:
        """Fetch the full-text XML for an open-access article."""
        url = f"{self.BASE_URL}/{article_id}/fullTextXML"
        return self._get_text(url)
