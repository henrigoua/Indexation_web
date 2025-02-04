import requests
import urllib.robotparser
import time
import logging
from urllib.parse import urljoin

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_page_content(url, timeout=10, retries=3, delay=2):
    """
    Récupère le contenu HTML d'une page web avec gestion des erreurs.

    Args:
        url (str): L'URL de la page web à récupérer.
        timeout (int): Temps maximum d'attente pour la requête.
        retries (int): Nombre de tentatives en cas d'échec.
        delay (int): Délai entre chaque tentative.

    Returns:
        str or None: Le contenu HTML de la page si réussi, None sinon.
    """
    for i in range(retries):
        try:
            logging.info(f"📡 Requête HTTP vers {url} (tentative {i+1}/{retries})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Lève une erreur pour les codes HTTP 4xx et 5xx
            return response.text
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout lors de l'accès à {url}, nouvelle tentative dans {delay} sec...")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur HTTP pour {url} : {e}")
            break  # Si ce n'est pas un timeout, on arrête tout de suite
        time.sleep(delay)  # Attente avant de réessayer
    return None

def can_fetch(url, retries=3, delay=2):
    """
    Vérifie si une URL peut être explorée selon les règles de robots.txt.

    Args:
        url (str): L'URL à vérifier.
        retries (int): Nombre de tentatives en cas d'échec.
        delay (int): Délai entre chaque tentative.

    Returns:
        bool: True si autorisé, False sinon.
    """
    try:
        base_url = "/".join(url.split('/')[:3])
        robots_url = urljoin(base_url, "robots.txt")
        rp = urllib.robotparser.RobotFileParser()

        for i in range(retries):
            try:
                logging.info(f"📄 Lecture du fichier robots.txt de {base_url} (tentative {i+1}/{retries})")
                rp.set_url(robots_url)
                rp.read()
                return rp.can_fetch("*", url)
            except Exception as e:
                logging.warning(f"Erreur de lecture de robots.txt ({base_url}) : {e}")
                time.sleep(delay)

        logging.warning(f"Impossible d'accéder à robots.txt de {base_url}. Par précaution, on bloque l'accès.")
        return False  

    except Exception as e:
        logging.error(f"Erreur critique lors du parsing de robots.txt : {e}")
        return False
