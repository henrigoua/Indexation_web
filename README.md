# **Projets : Indexation et Recherche**

Bienvenue dans la collection de projets réalisés dans le cadre de l'**apprentissage des systèmes d'indexation et des moteurs de recherche**. Ces projets illustrent différents aspects du traitement et de la recherche de données, depuis la collecte sur le web jusqu'à la création d'un moteur de recherche fonctionnel.

## **Structure des projets**

1. **[TP1 : Web Crawler](TP1/README.md)**
   - **Objectif** : Développer un crawler pour extraire automatiquement des données d'un site web.
   - **Principales fonctionnalités** :
     - Extraction des informations structurées.
     - Sauvegarde des données dans un format JSON réutilisable.
     - Gestion des URL pour éviter les doublons.
   - **Documentation complète** : Consultez le fichier [`TP1/README.md`](TP1/README.md).

2. **[TP2 : Développement d’un Index](tp2_developpement_index/README.md)**
   - **Objectif** : Construire un système d’indexation inversée permettant une recherche efficace dans un corpus de documents textuels.
   - **Principales fonctionnalités** :
     - Génération d’un index inversé basé sur des documents fournis.
     - Suppression des mots vides (stopwords) pour des résultats pertinents.
     - Recherche rapide en utilisant l’index généré.
   - **Documentation complète** : Consultez le fichier [`tp2_developpement_index/README.md`](tp2_developpement_index/README.md).

3. **[TP3 : Moteur de Recherche](TP3_Moteur_Recherche/README.md)**
   - **Objectif** : Mettre en œuvre un moteur de recherche avancé avec des fonctionnalités comme le filtrage, le classement, et une interface utilisateur.
   - **Principales fonctionnalités** :
     - Recherche par mots-clés et synonymes.
     - Classement des résultats par pertinence.
     - Interface utilisateur conviviale (basée sur FastAPI).
   - **Documentation complète** : Consultez le fichier [`TP3_Moteur_Recherche/README.md`](TP3_Moteur_Recherche/README.md).

---

## **Objectifs pédagogiques**

Ces projets couvrent un large éventail de concepts liés à l'indexation et à la recherche, notamment :

1. **Collecte de données :**
   - Compréhension des structures de sites web et extraction des informations utiles.
   - Utilisation de bibliothèques Python comme `requests` et `BeautifulSoup`.

2. **Indexation et traitement du texte :**
   - Création d’un index inversé pour optimiser la recherche.
   - Tokenisation et suppression des mots vides pour améliorer la précision.

3. **Recherche et classement :**
   - Implémentation d'algorithmes de recherche et de filtrage.
   - Classement des résultats en fonction de leur pertinence.
   - Introduction aux modèles de recherche comme BM25 et des approches personnalisées.

4. **Développement d'une API et d'une interface utilisateur :**
   - Construction d’une API REST avec FastAPI.
   - Création d’une interface utilisateur intuitive pour exécuter les recherches.

---

## **Organisation des projets**

Chaque projet est contenu dans son propre répertoire et comprend :
- Un fichier `README.md` décrivant le projet en détail.
- Une structure modulaire pour le code source, les données et les tests.
- Des tests unitaires pour valider les fonctionnalités.

---

## **Prérequis**

Les projets sont développés en Python et nécessitent :
- Python 3.8 ou version ultérieure.
- Les dépendances listées dans chaque fichier `requirements.txt`.

---

## **Exécution des projets**

1. Clonez le dépôt :
   ```bash
   git clone git@github.com:henrigoua/Indexation_web.git
   cd Indexation_web
   ```

2. Naviguez dans le dossier du projet souhaité (par exemple, TP3) :
   ```bash
   cd TP3_Moteur_Recherche
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Suivez les instructions spécifiques à chaque projet dans son `README.md`.

---

## **Contributions**

Ce dépôt est un projet éducatif. Si vous souhaitez contribuer :
1. Forkez le dépôt.
2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b feature/nouvelle_fonctionnalite
   ```
3. Soumettez une Pull Request.

---

## **Auteur**

- **Henri Goua** 

---

## **Licence**

Ce projet est sous licence MIT. Consultez le fichier [`LICENSE`](LICENSE) pour plus de détails.

---

