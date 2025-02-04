import unittest
import os
import json
from crawler import is_product_url, crawl, save_results_to_json

class TestCrawler(unittest.TestCase):

    def test_is_product_url(self):
        """ Teste si is_product_url() détecte correctement une URL de produit. """
        self.assertTrue(is_product_url("https://web-scraping.dev/product/1"))
        self.assertTrue(is_product_url("https://web-scraping.dev/product/123"))
        self.assertFalse(is_product_url("https://web-scraping.dev/products"))
        self.assertFalse(is_product_url("https://web-scraping.dev/"))

    def test_crawl_limited_pages(self):
        """ Teste le crawler avec un petit nombre de pages. """
        start_url = "https://books.toscrape.com/"
        max_pages = 3  # Petit crawl pour éviter la surcharge
        results = crawl(start_url, max_pages, delay=1, output_file="output/test_results.json")

        self.assertIsInstance(results, list)  # Vérifie que le crawler renvoie une liste
        self.assertGreater(len(results), 0, "Le crawler n'a extrait aucune donnée.")
        self.assertIn("title", results[0], "Les résultats ne contiennent pas de titre.")

    def test_save_results_to_json(self):
        """ Vérifie que les résultats sont bien sauvegardés en JSON. """
        test_data = [{"title": "Test Page", "url": "https://example.com"}]
        output_file = "output/test_results.json"

        save_results_to_json(test_data, output_file)

        # Vérifie que le fichier existe
        self.assertTrue(os.path.exists(output_file), "Le fichier JSON n'a pas été créé.")

        # Vérifie le contenu du fichier
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data, test_data, "Le fichier JSON ne contient pas les données attendues.")

    @classmethod
    def tearDownClass(cls):
        """ Nettoyage après les tests : suppression du fichier JSON de test. """
        output_file = "output/test_results.json"
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == "__main__":
    unittest.main()
