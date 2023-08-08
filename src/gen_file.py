import random
import time
from loguru import logger


def generate_file(filename="file.txt"):
    while True:
        # Generate a random character from the ASCII range of printable characters
        random_character = chr(random.randint(32, 126))
        try:
            # Open the file in write mode (or create it if it doesn't exist)
            with open(filename, "w") as file:
                file.write(random_character)
        except PermissionError:
            logger.info("permissions denied")
        print(f"Wrote character: {random_character}")

        # Wait for 1 second
        time.sleep(1)
