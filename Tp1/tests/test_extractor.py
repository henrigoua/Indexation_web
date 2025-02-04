import unittest
from extractor import extract_page_data

class TestExtractor(unittest.TestCase):

    def setUp(self):
        """ Définition des pages HTML de test pour éviter la répétition du code. """
        self.test_url = "https://example.com"
        self.sample_html = """<!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <p>Voici un exemple de contenu.</p>
            <a href="/produit1">Produit 1</a>
            <a href="https://autresite.com/externe">Lien externe</a>
            <a href="/contact">Contact</a>
        </body>
        </html>"""

    def test_extract_page_data_basic(self):
        """ Vérifie l'extraction des informations de base (titre, paragraphe). """
        page_data, _ = extract_page_data(self.test_url, self.sample_html)

        self.assertEqual(page_data["title"], "Test Page")
        self.assertEqual(page_data["url"], self.test_url)
        self.assertIn("Voici un exemple de contenu.", page_data["first_paragraph"])

    def test_extract_internal_links(self):
        """ Vérifie que seuls les liens internes sont extraits par défaut. """
        page_data, links = extract_page_data(self.test_url, self.sample_html)

        expected_links = [
            "https://example.com/produit1",
            "https://example.com/contact"
        ]
        self.assertCountEqual(links, expected_links)
        self.assertTrue(all(link.startswith(self.test_url) for link in links))

    def test_extract_external_links(self):
        """ Vérifie que les liens externes sont extraits si l'option est activée. """
        page_data, links = extract_page_data(self.test_url, self.sample_html, extract_external_links=True)

        expected_links = [
            "https://example.com/produit1",
            "https://example.com/contact",
            "https://autresite.com/externe"
        ]
        self.assertCountEqual(links, expected_links)

    def test_no_duplicate_links(self):
        """ Vérifie que les liens ne sont pas dupliqués. """
        duplicate_html = """<html><body>
            <a href="/produit1">Produit 1</a>
            <a href="/produit1">Produit 1 (dupliqué)</a>
        </body></html>"""
        page_data, links = extract_page_data(self.test_url, duplicate_html)

        self.assertEqual(len(links), 1)  # Un seul lien unique doit être extrait
        self.assertEqual(len(page_data["link_sources"]), 1)

    def test_empty_page(self):
        """ Vérifie le comportement sur une page vide. """
        page_data, links = extract_page_data(self.test_url, "")

        self.assertEqual(page_data["title"], "")
        self.assertEqual(page_data["first_paragraph"], "")
        self.assertEqual(len(links), 0)

if __name__ == "__main__":
    unittest.main()
