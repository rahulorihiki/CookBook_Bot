import re

def show_ingredients(state,query):
    return state.data['ingredients']

def show_tools(state,query):
    return state.data['tools']

def go_back(state,query):
    return state.previous()

def next_step(state,query):
    return state.next()

def repeat_step(state,query):
    return state.active_step()

def go_to_step(state, query):
    try:
        num = int(re.search(r'\d+', query).group())
        return state.jump_to_step(num - 1)
    except Exception as e:
        print("1")
        return "Sorry, something went wrong."

def ingredient_quantity(state, query):
    try:
        name = re.search(r'how much (?:of\s)?(\w+)', query).group(1)
        print(name)
        for ingredient in state.data['ingredients']:
            if name in ingredient:
                return ingredient
        return "Ingredient not found."
    except Exception as e:
        print("2")
        return "Sorry, something went wrong."

def what_is(state, query):
    try:
        name = re.search(r'what is (.+)', query).group(1)
        return f"https://www.google.com/search?q=what+is+a+{name.replace(' ', '+')}"
    except Exception as e:
        print("3")
        return "Sorry, something went wrong."

def how_to(state, query):
    try:
        method = re.search(r'how to(.+)', query).group(1)
        return f"https://www.youtube.com/results?search_query=how+do+i+{method.replace(' ', '+')}"
    except Exception as e:
        print("4")
        return "Sorry, something went wrong."

def how_to_do_that(state, query):
    current = state.active_step()
    return f"https://www.youtube.com/results?search_query=how+to+{current.replace(' ', '+')}"
