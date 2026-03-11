class WokwiService:
    @staticmethod
    def extract_project_id(url):
        """Extract Wokwi project id from full URL if needed for raw embedding"""
        if "projects/" in url:
            return url.split("projects/")[-1].strip("/")
        return None

    @staticmethod
    def generate_embed_url(project_id):
        """Standardize the embed format"""
        # For this design, we keep it simple by directly applying the URL to the iframe.
        # But this service could expand to hit Wokwi's API.
        return f"https://wokwi.com/projects/{project_id}"
