from bs4 import BeautifulSoup
import requests
import re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def get_details(url1):
    
    response = requests.get(url1, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')


    # Extract the recipe title
    title_element = soup.find('h1')
    recipe_title = title_element.text.strip() if title_element else "Title not found"


    potential_ingredient_sections = soup.find_all(lambda tag: tag.has_attr('class') and 
                                                any(re.search(r'ingredients', class_name) for class_name in tag['class']))
    ingredient_sections = []
    for tag in potential_ingredient_sections[0]:
        if hasattr(tag, 'find_all'):    
            for li in tag.find_all('li'):
                ingredient = li.get_text().strip()
                ingredient_sections.append(ingredient)


    potential_directions_sections = soup.find_all('ol')
    directions_sections = []
    for tag in potential_directions_sections:
        if hasattr(tag, 'find_all'):    
            for li in tag.find_all('li'):
                directions = li.get_text().replace('\n', '').replace('\xa0', '').strip()
                step = re.sub(r"Serious Eats.*$", "", directions)
                directions_sections.append(step)

    recipe_data = {
    "title": recipe_title,
    "ingredients": ingredient_sections,
    "steps": directions_sections
    }

    return(recipe_data)

