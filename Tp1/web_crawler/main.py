from crawler import crawl, save_results_to_json
import os


if __name__ == "__main__":
    start_url = "https://web-scraping.dev/products"
    max_pages = 50

    # Définition du chemin du fichier JSON dans le dossier output
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Création du dossier s'il n'existe pas
    output_file = os.path.join(output_dir, "results.json")

    print("Exécution du crawler...")
    results = crawl(start_url, max_pages, output_file=output_file)

    if results:
        print(f"Crawler a visité {len(results)} pages avec succès.")
    else:
        print("Le crawler n'a pas pu extraire de données.")

    print("Sauvegarde des résultats en JSON")
    save_results_to_json(results, output_file)
    print(f"Fichier JSON généré avec succès : {output_file}")
