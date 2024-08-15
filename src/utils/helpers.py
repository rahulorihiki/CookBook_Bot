import re

def show_ingredients(state,query):
    return state.data['ingredients']

def go_back(state,query):
    return state.previous_step()

def next_step(state,query):
    return state.next_step()

def repeat_step(state,query):
    return state.get_current_step()

def go_to_step(state, query):
    step_number = int(re.search(r'\d+', query).group())
    return state.go_to_step(step_number - 1)

def ingredient_quantity(state, query):
    ingredient_name = re.search(r'how much of (.+) do i need', query).group(1)
    for ingredient in state.data['ingredients']:
        if ingredient_name in ingredient:
            return ingredient
    return "Ingredient not found."

def what_is(state, query):
    tool_name = re.search(r'what is a (.+)', query).group(1)
    return f"https://www.google.com/search?q=what+is+a+{tool_name.replace(' ', '+')}"

def how_to(state, query):
    technique = re.search(r'how do i (.+)', query).group(1)
    return f"https://www.youtube.com/results?search_query=how+do+i+{technique.replace(' ', '+')}"

def how_to_do_that(state, query):
    current_step = state.get_current_step()
    return f"https://www.youtube.com/results?search_query=how+to+{current_step.replace(' ', '+')}"
