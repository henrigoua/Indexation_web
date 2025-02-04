from bs4 import BeautifulSoup
import requests

def scrape_product_details(url):
    """
    Scrape product details from a given URL.

    This function extracts the product price and image URLs from an e-commerce webpage.

    Args:
        url (str): The URL of the product page.

    Returns:
        tuple: A tuple containing:
            - price (str): The extracted price of the product.
            - image_urls (list): A list of image URLs associated with the product.
    """
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the product price
    price_element = soup.find("span", class_="product-price mt-5 fs-1 text-success")
    price = price_element.text.strip() if price_element else "Price not found"

    # Extract product images
    image_tags = soup.find_all("img", class_="img-responsive product-img")
    image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

    return price, image_urls
