from itertools import product

# Variables
symbols = ["Harry", "Hermione", "Ron"]

def knowledge(Harry, Hermione, Ron):
    # Example rules:
    # If Hermione is in the library, then Harry is in the library
    rule1 = (not Hermione) or Harry

    # Hermione is in the library
    rule2 = Hermione

    return rule1 and rule2

# Try all possible truth assignments
for values in product([False, True], repeat=len(symbols)):
    Harry, Hermione, Ron = values

    if knowledge(Harry, Hermione, Ron):
        print("Valid model:")
        print(f"Harry = {Harry}")
        print(f"Hermione = {Hermione}")
        print(f"Ron = {Ron}")
        print()