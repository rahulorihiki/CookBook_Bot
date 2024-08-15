from src.components.scraper import get_details
from src.utils.models import State, CommandHandler
import os
import sys
from src.logging import logger

def error_handler(message):
    print(message)
    logger.error(message)
    print("Press 1 to try again or 2 to exit")
    logger.info("User asked to try again or exit")
    choice = input()
    if choice == "1":
        logger.info("User chose to try again")
        os.system('cls' if os.name == 'nt' else 'clear')
        cookbook_bot()
    else:
        # Exit the program
        logger.info("User chose to exit the program")
        sys.exit("Exiting the program, Thank you for using the cookbook bot!")

def cookbook_bot():
    print()
    logger.info(">>>>>>>>>>> Starting the cookbook bot <<<<<<<<<<<")
    print("Hello! I am the cookbook bot!\n")
    print("I can help you understand and guide through the recipe of your favourite dish.\n")
    print("Can you provide the link of the recipe you want me to guide you through?")

    # Get the link of the recipe from the user
    recipe_link = input()
    logger.info(f"User provided the recipe link: {recipe_link}")
    # Get the details from the link
    try:
        details = get_details(recipe_link)
    except Exception as e:
        error_handler("Sorry, I am unable to fetch the details. Please try again later.")
        logger.error(f"Error occurred: {e}")

    print()
    print("The recipe details has been fetched successfully.\n")
    logger.info(f"Recipe details fetched successfully titled: {details['title']}")
    print(f"Alright. So let's start working with {details['title']}. \n")

    state = State(details)
    handler = CommandHandler()

    while True:

        query = input("Q) How may I help you? \n")
        logger.info(f"User asked: {query}")
        if "exit" in query.lower():
            logger.info("User chose to exit the program")
            print("Exiting the program, Thank you for using the cookbook bot!")
            break
        response = handler.handle(state, query)
        print()
        print("--> " + str(response))
        logger.info(f"Response: {response}")
        print()


if __name__ == "__main__":
    cookbook_bot()