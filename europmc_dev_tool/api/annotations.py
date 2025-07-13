from .client import BaseClient
from urllib.parse import urlencode

class AnnotationsClient(BaseClient):
    """
    Client for the Europe PMC Annotations API.
    See: https://europepmc.org/AnnotationsApi
    """
    BASE_URL = "https://www.ebi.ac.uk/europepmc/annotations_api"

    def get_by_article_ids(self, article_ids: list, provider: str = None) -> dict:
        """
        Retrieve text-mined annotations for given article IDs.
        IDs should be in the format: SOURCE:ID, e.g., PMC:11704132
        """
        url = f"{self.BASE_URL}/annotationsByArticleIds"
        params = {
            "articleIds": ",".join(article_ids),
            "provider": provider
        }
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}
        params = self._build_params(params)
        return self._get(url, params)

    def get_by_entity(self, entity: str, provider: str = None) -> dict:
        """
        Find articles that cite a specific entity (e.g., gene, chemical).
        """
        url = f"{self.BASE_URL}/annotationsByEntity"
        params = {"entity": entity, "provider": provider}
        params = {k: v for k, v in params.items() if v is not None}
        params = self._build_params(params)
        return self._get(url, params)

    def get_by_section_and_or_type(self, annotation_type: str, subtype: str = None, section: str = None, provider: str = None, filter: int = 1, page_size: int = 4, cursor_mark: str = "0.0") -> dict:
        """
        Get annotations of a specific type, optionally filtered by subtype and section.
        """
        
        params = {
            "type": annotation_type,
            "subtype": subtype,
            "section": section,
            "provider": provider,
            "filter": filter,
            "pageSize": page_size,
            "cursorMark": cursor_mark,
            "format": "json"
        }
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}
        
        url = f"{self.BASE_URL}/annotationsBySectionAndOrType?{urlencode(params)}"
        
        return self._get(url)
