import functools
import random


def in_conflict(column, row, other_column, other_row):
    # Checks if two locations are in conflict with each other
    # column: Column of queen 1
    # row: Row of queen 1
    # other_column: Column of queen 2
    # other_row: Row of queen 2
    # Returns True if the queens are in conflict, else False

    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    # Checks if the given row and column correspond to a queen that is in conflict with another queen
    # row: Row of the queen to be checked
    # column: Column of the queen to be checked
    # board: Board with all the queens
    # Returns True if the queen is in conflict, else False

    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True

    return False


def count_conflicts(board):
    # Counts the number of queens in conflict with each other
    # board: The board with all the queens on it
    # Returns The number of conflicts

    count = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen + 1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                count += 1

    return count


def evaluate_state(board):
    # Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    # (nqueens-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    # (nqueens-1)*nqueens/2 - countConflicts()
    # board: list/array representation of columns and the row of the queen on that column
    # Returns evaluation score

    return (len(board) - 1) * len(board) / 2 - count_conflicts(board)


def print_board(board):
    # Prints the board in a human-readable format in the terminal
    # board: The board with all the queens

    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    # nqueens: integer for the number of queens on the board
    # Returns list/array representation of columns and the row of the queen on that column

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens - 1))

    return board


def genetic_algorithm(board):
    counter = 0
    initial_population_size = 100000  # Must be multiple of 100
    number_of_parents = 500  # Must be multiple of 10
    mutation_rate = 0.01  # e.g. 0.1 = 10% for each individual gene
    max_generations = 10000
    elitism_factor = 2  # max % of parents capable of being included in next generation, 2 = 50%, 4 = 25%, 10 = 10%
    initial_population = []
    population_value = []
    optimum = (len(board) - 1) * len(board) / 2

    # Initialize a random population
    for x in range(initial_population_size):
        x = init_board(len(board))
        initial_population.append(x)

    # Evaluate each member of the population (fitness)
    for x in range(initial_population_size):
        population_value.append(evaluate_state(initial_population[x]))

    # Choose the most suitable members of the population (i.e. parents)
    parents = [x for _, x in sorted(zip(population_value, initial_population), key=lambda pair: pair[0], reverse=True)]
    parents = parents[:number_of_parents]

    # --- LOOP START ---
    while True:
        parents_value = []
        children = []
        final_population_value = []

        # Print attempt number and evaluation score
        counter += 1
        print('iteration ' + str(counter) + ': evaluation = ' + str(evaluate_state(board)))
        if counter == max_generations:  # Give up after max generations.
            break

        # Evaluate each parent
        for x in range(number_of_parents):
            parents_value.append(evaluate_state(parents[x]))

        # Select 2 parents (more suitable = more chances of being selected) and make 2 children
        # Number of children made = number of parents
        for x in range(0, number_of_parents, 2):
            num = random.randint(1, (len(board) - 1))  # Randomly select the crossover point

            parent_1 = random.choices(parents, weights=parents_value, k=1)

            while True:  # Make sure it selects a different parent
                parent_2 = random.choices(parents, weights=parents_value, k=1)
                if not functools.reduce(lambda i, j: i and j, map(lambda m, k: m == k, parent_1, parent_2), True):
                    break

            children.append(parent_1[0][:num] + parent_2[0][-(len(board) - num):])
            children.append(parent_2[0][:num] + parent_1[0][-(len(board) - num):])

        # Initialize final population (children)
        final_population = children.copy()

        # Change the elitism factor every x hundred generations
        if (counter % 300) == 0:
            elitism_factor = 10
        elif (counter % 200) == 0:
            elitism_factor = 4
        elif (counter % 100) == 0:
            elitism_factor = 2

        # Implement elitism - % of previous generation (parents) can be included in next generation (children)
        # From total elitism %, the second half will have a chance of being mutated
        # and the first half will not be mutated at all in every cycle
        # Here we append the second half of elite parents (that will be mutated)
        parents = parents[:int((number_of_parents / elitism_factor))]
        for x in range(int((number_of_parents / elitism_factor) / 2), int(number_of_parents / elitism_factor)):
            final_population.append(parents[x])

        # Change the mutation rate every x thousand generations
        if (counter % 3000) == 0:
            mutation_rate = 0.01
        elif (counter % 2000) == 0:
            mutation_rate = 0.05
        elif (counter % 1000) == 0:
            if (counter % 200) == 0:
                mutation_rate = 0.1
            elif (counter % 100) == 0:
                mutation_rate = 0.02

        # Mutate each gene in final population based on fixed rate
        for x in range(number_of_parents):
            for y in range(len(board)):
                num_2 = random.uniform(0, 1)
                if num_2 < mutation_rate:
                    while True:  # Make sure it mutates the gene (if the new gene is the same as the old)
                        num_3 = random.randint(0, (len(board) - 1))
                        if final_population[x][y] != num_3:
                            final_population[x][y] = num_3
                            break

        # Every 100 generations create random smaller pool of parents and append to current population
        if (counter % 100) == 0:
            for x in range(int(initial_population_size / 100)):
                random_board = init_board(len(board))
                final_population.append(random_board)

        # Append first half of elite parents (no mutation)
        for x in range(int((number_of_parents / elitism_factor) / 2)):
            final_population.append(parents[x])

        # Evaluate final population
        for x in range(int(number_of_parents + (number_of_parents / elitism_factor))):
            final_population_value.append(evaluate_state(final_population[x]))

        # Keep the most suitable members for the final population
        final_population = [x for _, x in sorted(zip(final_population_value, final_population), key=lambda pair: pair[0], reverse=True)]
        final_population = final_population[:number_of_parents]

        # Rearrange the board based on final population (try to solve)
        for x in range(number_of_parents):
            for column, row in enumerate(board):
                board[column] = final_population[x][column]
            if evaluate_state(board) == optimum:
                break

        # If solution is found then exit loop
        if evaluate_state(board) == optimum:
            break
        else:
            parents = final_population.copy()
    # --- LOOP END -----

    # Print message if problem is solved
    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    # Print final state of the board
    print('Final state is:')
    print_board(board)


def main():
    print('How many queens? (4-100)')
    n_queens = int(input())
    if 4 <= n_queens <= 100:
        board = init_board(n_queens)
        genetic_algorithm(board)
    else:
        print('Must be between 4 and 100')


if __name__ == "__main__":
    main()
