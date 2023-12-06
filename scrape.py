import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os
import shutil

url = 'https://animalcorner.org/animals/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

animal_links = []
for link in soup.find_all('a', href=True):
    if '/animals/' in link['href'] and link['href'] not in animal_links:
        animal_links.append(link['href'])

def scrape_animal_page(url):
    response = requests.get(url)
    page_soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract data like name and image url
    name = page_soup.find('h1').text
    image = page_soup.find('img')['src'] if page_soup.find('img') else None

    print(f"Scraping {name} from {url}")

    # Download the image and save it to a local file
    if image and not image.startswith('data:'):
        print(f"Downloading image from {image}")
        image_response = requests.get(image, stream=True)
        if image_response.status_code == 200:
            # Create a directory to store the images if it doesn't already exist
            if not os.path.exists('images'):
                os.makedirs('images')

            # Use the last part of the image URL as the file name
            image_file_name = os.path.join('images', image.split('/')[-1])
            with open(image_file_name, 'wb') as f:
                image_response.raw.decode_content = True
                shutil.copyfileobj(image_response.raw, f)

            print(f"Saved image to {image_file_name}")

            # Use the local file path as the image URL
            image = image_file_name
        else:
            print(f"Failed to download image from {image}")
    else:
        print(f"No image to download for {name}")

    return {
        'name': name,
        'image': image,
    }

animal_data = []
for link in animal_links:
    full_link = urljoin('https://animalcorner.org', link)  # Ensure correct URL format
    animal_info = scrape_animal_page(full_link)
    animal_data.append(animal_info)

with open('animal_data.json', 'w') as f:
    json.dump(animal_data, f)