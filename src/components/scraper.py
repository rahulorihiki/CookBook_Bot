from bs4 import BeautifulSoup
import requests
import re
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Header for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
def get_details(url1):
    # Fetch the page
    response = requests.get(url1, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the recipe title
    title_element = soup.find('h1')
    recipe_title = title_element.text.strip() if title_element else "Title not found"
    print("Title: ", recipe_title)

    # Find ingredient sections
    potential_ingredient_sections = soup.find_all(lambda tag: tag.has_attr('class') and 
                                                  any(re.search(r'ingredients', class_name) for class_name in tag['class']))
    ingredient_sections = []
    if potential_ingredient_sections:
        for tag in potential_ingredient_sections[0]:
            if hasattr(tag, 'find_all'):
                for li in tag.find_all('li'):
                    ingredient = li.get_text().strip()
                    ingredient_sections.append(ingredient)

    # Find direction sections
    potential_directions_sections = soup.find_all('ol')
    directions_sections = []
    for tag in potential_directions_sections:
        if hasattr(tag, 'find_all'):
            for li in tag.find_all('li'):
                directions = li.get_text().replace('\n', '').replace('\t', '').replace('\xa0', '').strip()
                step = re.sub(r"Serious Eats.*$", "", directions)
                directions_sections.append(step.rstrip())

    # Lowercase the direction text and analyze with spaCy
    recipe_text = " ".join(directions_sections).lower()
    doc = nlp(recipe_text)
    tools = set()

    # Known tools and non-tool keywords
    known_tools = {"knife", "cutting board", "mixer", "spatula", "whisk", "bowl", "saucepan", 
                   "skillet", "pot", "oven", "tongs", "measuring cup", "measuring spoon",
                   "baking sheet", "rolling pin", "colander", "sieve", "grater", "zester",
                   "blender", "food processor", "spoon", "fork", "plate", "serving spoon",
                   "pan", "cake pan", "loaf pan", "muffin tin", "pie dish", "spoon", "scissor", 
                   "tray", "stand mixer", "basket", "dutch oven", "wooden spoon", "dish towel",
                   "pot holder", "trivet", "steamer", "steamer basket"}
    non_tool_keywords = {"hand", "fingers", "heat", "oven", "water", "seasoning", 
                         "ingredients", "minutes", "end", "wrapper", "baking", "piece", 
                         "sides", "small", "medium", "tablespoon", "cup", "time", "amount", 
                         "salt", "masa harina", "corn husks", "towel", "attachment"}

    # Extract tools based on patterns
    for token in doc:
        if token.dep_ in ["dobj", "pobj", "nsubj"] and (token.head.lemma_ in ["use", "cut", "add", "spread"] or token.text in known_tools):
            if token.text in known_tools:
                tools.add(token.text)
        if token.dep_ == "pobj" and token.head.text in ["with", "using"]:
            if token.text in known_tools:
                tools.add(token.text)

    for chunk in doc.noun_chunks:
        if chunk.root.text in known_tools and len(chunk.text.split()) <= 3:
            tools.add(chunk.root.text)

    recipe_data = {
        "title": recipe_title,
        "ingredients": ingredient_sections,
        "steps": directions_sections,
        "tools": list(tools)
    }

    return recipe_data


