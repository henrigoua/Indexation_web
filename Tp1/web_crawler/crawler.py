import time
import os
import json
import logging
import collections
from urllib.parse import urljoin, urlparse
from utils import can_fetch, get_page_content
from extractor import extract_page_data

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def is_product_url(url):
    """
    Vérifie si une URL correspond à une page produit.

    Args:
        url (str): L'URL à analyser.

    Returns:
        bool: True si c'est une URL de produit, False sinon.
    """
    parsed_url = urlparse(url)
    return "product" in parsed_url.path.lower()  # Vérifie si "product" est dans l'URL


def crawl(start_url, max_pages=50, delay=1, output_file=None):
    """
    Explore les pages web d'un site, extrait les informations pertinentes,
    respecte la notion de politesse et les règles du robots.txt.

    Args:
        start_url (str): URL de départ du crawl.
        max_pages (int): Nombre maximum de pages à visiter.
        delay (int): Temps d'attente entre chaque requête (en secondes).
        output_file (str): Chemin du fichier JSON pour sauvegarder les résultats.

    Returns:
        list: Liste des résultats extraits.
    """
    start_time = time.time()

    # Vérification et création du chemin de sortie
    if output_file is None:
        output_file = os.path.join("output", "results.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    logging.info(f"🚀 Démarrage du crawl sur {start_url} avec une limite de {max_pages} pages.")

    visited_urls = set()
    urls_to_visit = collections.deque([start_url])
    results = []
    pages_crawled = 0
    product_pages_crawled = 0

    try:
        while urls_to_visit and pages_crawled < max_pages:
            url = urls_to_visit.popleft()

            if url in visited_urls:
                continue

            if not can_fetch(url):
                logging.warning(f"Accès interdit par robots.txt : {url}")
                visited_urls.add(url)
                continue

            logging.info(f"🔍 Crawling {url}... ({pages_crawled + 1}/{max_pages})")
            content = get_page_content(url)
            time.sleep(delay)

            if content:
                page_data, new_links = extract_page_data(url, content)
                results.append(page_data)
                visited_urls.add(url)
                pages_crawled += 1

                if is_product_url(url):
                    product_pages_crawled += 1

                # Ajout des nouveaux liens à explorer
                unique_links = set()  # Évite les doublons
                for link in new_links:
                    full_url = urljoin(url, link)
                    if full_url not in visited_urls and full_url not in unique_links:
                        unique_links.add(full_url)
                        if is_product_url(full_url):
                            urls_to_visit.appendleft(full_url)  # Priorité aux pages produits
                        else:
                            urls_to_visit.append(full_url)

            else:
                logging.error(f"Échec du téléchargement de {url}")
                visited_urls.add(url)

    except Exception as e:
        logging.error(f"Erreur critique pendant le crawling : {e}")

    save_results_to_json(results, output_file)

    end_time = time.time()
    duration = round(end_time - start_time, 2)
    logging.info(f"Fin du crawl en {duration} secondes. {pages_crawled} pages explorées, dont {product_pages_crawled} pages produits.")
    logging.info(f"Résultats sauvegardés dans {output_file}")

    return results


def save_results_to_json(results, filename="output/results.json"):
    """
    Enregistre les résultats du crawl dans un fichier JSON.

    Args:
        results (list): La liste des résultats extraits.
        filename (str): Le nom du fichier de sortie.
    """
    try:
        # Vérifier et créer le dossier si nécessaire
        output_dir = os.path.dirname(filename)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Écriture des résultats dans un fichier JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        logging.info(f"✅ Résultats sauvegardés avec succès dans {filename}")

    except Exception as e:
        logging.error(f"❌ Impossible d'enregistrer les résultats dans {filename} : {e}")
        logging.info("💡 Vérifiez que le chemin d'accès est correct et que vous avez les permissions nécessaires.")


