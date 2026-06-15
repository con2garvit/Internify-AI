def solve_puzzle(variables, domains, constraints):
    assignment = {}

    def is_valid(variable, value):
        temp_assignment = assignment.copy()
        temp_assignment[variable] = value

        for constraint in constraints:
            if not constraint(temp_assignment):
                return False
        return True

    def backtrack():
        if len(assignment) == len(variables):
            return assignment

        unassigned = [v for v in variables if v not in assignment]
        variable = unassigned[0]

        for value in domains[variable]:
            if is_valid(variable, value):
                assignment[variable] = value
                result = backtrack()

                if result:
                    return result

                del assignment[variable]

        return None

    return backtrack()


# Example Puzzle:
# A, B, C must have different values from {1, 2, 3}
variables = ["A", "B", "C"]

domains = {
    "A": [1, 2, 3],
    "B": [1, 2, 3],
    "C": [1, 2, 3]
}

constraints = [
    lambda a: len(set(a.values())) == len(a.values())
]

solution = solve_puzzle(variables, domains, constraints)

print("Solution:", solution)