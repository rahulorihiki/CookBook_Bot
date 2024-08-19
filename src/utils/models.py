from src.utils.helpers import show_ingredients, go_back, next_step, repeat_step, go_to_step, ingredient_quantity, what_is, how_to, how_to_do_that, show_tools
import spacy

# Load the medium spaCy model
nlp = spacy.load("en_core_web_md")

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
        print(self.step_counter,end=" ")
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


# Using SBERT method
from sentence_transformers import SentenceTransformer, util

class CommandHandler:
    def __init__(self):
        self.commands = {
            "go over all the ingredients": show_ingredients,
            "go over all the tools": show_tools,
            "show previous step": go_back,
            "show next step": next_step,
            "repeat step again": repeat_step,
            "go to step": go_to_step,
            "how much": ingredient_quantity,
            "what is": what_is,
            "how to": how_to,
            "explain how do that": how_to_do_that
        }
        
        # Load the SBERT model (which is based on BERT/RoBERTa)
        self.model = SentenceTransformer('stsb-roberta-base')
        
        # Precompute embeddings for each command
        self.command_embeddings = {cmd: self.model.encode(cmd) for cmd in self.commands}

    def handle(self, state, query):
        
        # Lowercase the query for better matching
        query_lower = query.lower()
        # Rule-based approach for specific commands
        if "how much" in query_lower:
            return self.commands["how much"](state, query)
        
        if "how to" in query_lower:
            return self.commands["how to"](state, query)
        
        # Compute the embedding for the user's query
        query_embedding = self.model.encode(query_lower)
        
        # Initialize variables to find the best match
        best_match, best_score = None, 0
        
        # Compare the user's query with each command
        for command, cmd_embedding in self.command_embeddings.items():
            # Compute cosine similarity
            score = util.pytorch_cos_sim(query_embedding, cmd_embedding)
            if score > best_score:
                best_match, best_score = command, score
        
        # Threshold to determine if a match is good enough (tune based on testing)
        if best_score > 0.2:  # Adjust threshold as needed
            return self.commands[best_match](state, query)

        return "Sorry, I didn't understand that question."
