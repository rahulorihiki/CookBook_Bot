from src.utils.helpers import show_ingredients, go_back, next_step, repeat_step, go_to_step, ingredient_quantity, what_is, how_to, how_to_do_that

class State:
    def __init__(self, data):
        self.data = data
        self.step_counter = 0

    def _update_step_counter(self, new_step):
        """Safely update the step counter based on bounds."""
        if 0 <= new_step < len(self.data['steps']):
            self.step_counter = new_step
        else:
            return "Step not available."
        return self.active_step()

    def active_step(self):
        """Return the current active step."""
        return self.data['steps'][self.step_counter]

    def next(self):
        """Move to the next step if possible."""
        return self._update_step_counter(self.step_counter + 1)

    def previous(self):
        """Move to the previous step if possible."""
        return self._update_step_counter(self.step_counter - 1)

    def jump_to_step(self, step_number):
        """Jump to a specific step number."""
        return self._update_step_counter(step_number)


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