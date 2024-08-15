import re

def show_ingredients(state,query):
    return state.data['ingredients']

def go_back(state,query):
    return state.previous()

def next_step(state,query):
    return state.next()

def repeat_step(state,query):
    return state.active_step()

def go_to_step(state, query):
    num = int(re.search(r'\d+', query).group())
    return state.jump_to_step(num - 1)

def ingredient_quantity(state, query):
    name = re.search(r'how much of (.+) do i need', query).group(1)
    for ingredient in state.data['ingredients']:
        if name in ingredient:
            return ingredient
    return "Ingredient not found."

def what_is(state, query):
    name = re.search(r'what is a (.+)', query).group(1)
    return f"https://www.google.com/search?q=what+is+a+{name.replace(' ', '+')}"

def how_to(state, query):
    method = re.search(r'how do i (.+)', query).group(1)
    return f"https://www.youtube.com/results?search_query=how+do+i+{method.replace(' ', '+')}"

def how_to_do_that(state, query):
    current = state.active_step()
    return f"https://www.youtube.com/results?search_query=how+to+{current.replace(' ', '+')}"
