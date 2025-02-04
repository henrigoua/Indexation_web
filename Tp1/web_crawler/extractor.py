from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_page_data(url, content, extract_external_links=False):
    """
    Extrait le titre, le premier paragraphe et les liens internes d'une page HTML.
    Option pour extraire aussi les liens externes.

    Args:
        url (str): L'URL de la page web.
        content (str): Le contenu HTML de la page.
        extract_external_links (bool): Si True, extrait aussi les liens externes.

    Returns:
        tuple: Un dictionnaire avec les données extraites et une liste des nouveaux liens.
    """
    try:
        soup = BeautifulSoup(content, 'html.parser')

        # Extraction du titre (assure que ce n'est jamais None)
        title = soup.find('title')
        title = title.text.strip() if title else ""

        # Extraction du premier paragraphe (assure que ce n'est jamais None)
        first_paragraph = soup.find('p')
        first_paragraph = first_paragraph.text.strip() if first_paragraph else ""

        # Détermination du domaine de base
        base_domain = urlparse(url).netloc

        # Stockage des liens (évite les doublons)
        links = set()
        link_sources = set()

        for link in soup.find_all('a', href=True):
            full_link = urljoin(url, link['href']).strip()

            # Vérifier si le lien est valide
            if full_link and not full_link.startswith("#"):
                link_domain = urlparse(full_link).netloc

                # Ajouter uniquement les liens internes ou externes selon `extract_external_links`
                if extract_external_links or link_domain == base_domain:
                    links.add(full_link)
                    link_sources.add((url, full_link))  # Stockage temporaire sous forme de tuple

        # Conversion des sets en listes pour JSON
        return {
            "title": title,
            "url": url,
            "first_paragraph": first_paragraph,
            "links": list(links),
            "link_sources": [{"source_url": src, "target_url": tgt} for src, tgt in link_sources]
        }, list(links)

    except Exception as e:
        logging.error(f"Erreur lors de l'extraction des données pour {url}: {e}")
        return {
            "title": "",
            "url": url,
            "first_paragraph": "",
            "links": [],
            "link_sources": []
        }, []

