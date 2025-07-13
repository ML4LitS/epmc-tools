from .client import BaseClient

class OAIClient(BaseClient):
    """
    Client for the Europe PMC OAI-PMH service.
    """
    BASE_URL = "https://europepmc.org/oai.cgi"

    def harvest(self, verb: str = "ListRecords", metadata_prefix: str = "oai_dc", from_date: str = None, until: str = None, set_spec: str = None) -> str:
        """Harvest metadata via OAI-PMH."""
        params = {"verb": verb, "metadataPrefix": metadata_prefix}
        if from_date:
            params["from"] = from_date
        if until:
            params["until"] = until
        if set_spec:
            params["set"] = set_spec
        
        # OAI-PMH returns XML, so we use _get_text
        return self._get_text(self.BASE_URL, params)
