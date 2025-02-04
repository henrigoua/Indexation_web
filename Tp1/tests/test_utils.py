import unittest
import requests_mock
from utils import get_page_content, can_fetch

class TestUtils(unittest.TestCase):

    def setUp(self):
        """ Définition des URL de test. """
        self.test_url = "https://example.com"
        self.robots_txt_url = "https://example.com/robots.txt"

    def test_get_page_content_success(self):
        """ Vérifie si `get_page_content` récupère bien le contenu HTML d'une page valide. """
        with requests_mock.Mocker() as m:
            m.get(self.test_url, text="<html><body>Page test</body></html>", status_code=200)

            content = get_page_content(self.test_url)
            self.assertIsNotNone(content)
            self.assertIn("Page test", content)

    def test_get_page_content_timeout(self):
        """ Vérifie que `get_page_content` gère bien un timeout. """
        with requests_mock.Mocker() as m:
            m.get(self.test_url, exc=requests_mock.exceptions.ConnectTimeout)

            content = get_page_content(self.test_url, retries=1)  # Une seule tentative
            self.assertIsNone(content)

    def test_get_page_content_404(self):
        """ Vérifie que `get_page_content` renvoie None si la page renvoie une erreur HTTP 404. """
        with requests_mock.Mocker() as m:
            m.get(self.test_url, status_code=404)

            content = get_page_content(self.test_url)
            self.assertIsNone(content)

    def test_can_fetch_allowed(self):
        """ Vérifie si `can_fetch` détecte une URL autorisée par robots.txt. """
        robots_content = "User-agent: *\nAllow: /"
        with requests_mock.Mocker() as m:
            m.get(self.robots_txt_url, text=robots_content)

            is_allowed = can_fetch(self.test_url)
            self.assertTrue(is_allowed)

    def test_can_fetch_disallowed(self):
        """ Vérifie si `can_fetch` bloque une URL interdite par robots.txt. """
        robots_content = "User-agent: *\nDisallow: /"
        with requests_mock.Mocker() as m:
            m.get(self.robots_txt_url, text=robots_content)

            is_allowed = can_fetch(self.test_url)
            self.assertFalse(is_allowed)

    def test_can_fetch_no_robots_txt(self):
        """ Vérifie que `can_fetch` renvoie False si le fichier robots.txt est inaccessible. """
        with requests_mock.Mocker() as m:
            m.get(self.robots_txt_url, status_code=404)

            is_allowed = can_fetch(self.test_url)
            self.assertFalse(is_allowed)

if __name__ == "__main__":
    unittest.main()
