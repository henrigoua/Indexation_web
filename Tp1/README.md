
# **INDEXATION_WEB**

## **Description**
`INDEXATION_WEB` est un projet Python conçu pour effectuer du web scraping et de l'indexation. Il permet d'explorer des sites web, d'extraire des informations pertinentes (comme les titres, paragraphes et liens), et de les sauvegarder dans des fichiers JSON. Le projet respecte les règles définies dans le fichier `robots.txt` des sites web pour garantir un scraping éthique.

---

## **Fonctionnalités**
- Crawling d’un site web à partir d’une URL de départ.
- Extraction des informations suivantes :
  - Titre de la page.
  - Premier paragraphe.
  - Liens internes et externes.
- Respect des règles de politesse (`robots.txt`) et gestion des délais entre les requêtes.
- Sauvegarde des résultats dans des fichiers JSON pour analyse ou utilisation ultérieure.
- Tests unitaires pour garantir la fiabilité des fonctions principales.

---

## **Structure du projet**
```
INDEXATION_WEB/
│
├── output/                 # Dossier contenant les résultats du crawling
│   ├── results.json        # Résultats générés par le crawler
│   ├── results_ref.json    # Résultats de référence pour les tests
│
├── tests/                  # Dossier contenant les tests unitaires
│   ├── test_crawler.py     # Tests pour le module crawler.py
│   ├── test_extractor.py   # Tests pour le module extractor.py
│   ├── test_utils.py       # Tests pour le module utils.py
│
├── web_crawler/            # Dossier contenant le code source
│   ├── crawler.py          # Module principal pour le crawling
│   ├── extractor.py        # Module pour extraire les données des pages
│   ├── utils.py            # Fonctions utilitaires pour HTTP et robots.txt
│   ├── main.py             # Point d’entrée principal pour exécuter le projet
│
├── README.md               # Documentation du projet
├── requirements.txt        # Liste des dépendances Python
```

---

## **Installation**

### **Prérequis**
- Python 3.8 ou une version ultérieure.
- Un gestionnaire de paquets comme `pip`.

### **Étapes**
1. Clone le dépôt :
   ```bash
   git clone https://github.com/henrigoua/Indexation_web.git
   cd indexation_web
   ```

2. Crée un environnement virtuel et active-le :
   ```bash
   python -m venv venv
   source venv/bin/activate    # Sur Linux/Mac
   venv\Scripts\activate       # Sur Windows
   ```

3. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Assure-vous que la structure des dossiers est conforme.

---

## **Utilisation**

### **Exécution du crawler**
Pour démarrer le crawler, exécute le fichier `main.py` :
```bash
python web_crawler/main.py
```
Par défaut, les résultats sont sauvegardés dans `output/results.json`.

### **Personnalisation**
vous pouvez modifier les paramètres suivants directement dans le fichier `main.py` :
- **start_url** : URL de départ du crawl.
- **max_pages** : Nombre maximum de pages à explorer.
- **delay** : Délai (en secondes) entre les requêtes pour éviter la surcharge du serveur.

---

## **Tests**
Pour exécuter les tests unitaires :
```bash
python -m unittest discover -s tests
```

Cela lancera tous les tests définis dans le dossier `tests`.

---

## **Contributeurs**
- **Goua Beedi** 

---

## **Licence**
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

