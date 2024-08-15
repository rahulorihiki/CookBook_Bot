from src.utils.helpers import show_ingredients, go_back, next_step, repeat_step, go_to_step, ingredient_quantity, what_is, how_to, how_to_do_that

class State:
    def __init__(self, data):
        self.data = data
        self.current_step = 0

    def get_current_step(self):
        return self.data['steps'][self.current_step]

    def next_step(self):
        if self.current_step < len(self.data['steps']) - 1:
            self.current_step += 1
        return self.get_current_step()

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
        return self.get_current_step()

    def go_to_step(self, step_number):
        if 0 <= step_number < len(self.data['steps']):
            self.current_step = step_number
        return self.get_current_step()


class CommandHandler:
    def __init__(self):
        self.commands = {
            "go over all the ingredients": show_ingredients,
            "show previous step": go_back,
            "show next step": next_step,
            "show this step again": repeat_step,
            "take me to the": go_to_step,
            "how much": ingredient_quantity,
            "what is a": what_is,
            "how do i do that": how_to_do_that,
            "how do i": how_to
        }

    def handle(self, state, query):
        query = query.lower()
        for key, command in self.commands.items():
            if key in query:
                return command(state, query)
        return "Sorry, I didn't understand that question."