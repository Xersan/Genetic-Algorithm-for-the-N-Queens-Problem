
# Genetic Algorithm for the N Queens Problem

### Implementation of the Genetic Algorithm in Python to solve the N-Queens Problem  

<br>

## Introduction

#### N-Queens Problem
Place N queens on an N x N chessboard so that no queen can attack another.

#### Genetic Algorithm
The Genetic Algorithm emulates the natural selection process. Each member of the population represents a possible solution to our problem. With every generation the population is renewed. This new population is, in theory, a more suitable solution to the problem, an “evolved” population. Given enough generations, the problem should eventually be solved or reach a plateau where further optimization is not possible.

<br>

## Explanation

#### Some important concepts (as applied in this implementation)
- **Population:** a collection of members
- **Member:** a possible solution to the problem (i.e., a way to place the queens on the board)
- **Gene:** each member has a number of genes that represent the row of the queen on that column (e.g., a member with its 3rd gene = 2, means that on the third column of the board, the queen is placed on the second row). Basically, a string of numbers like [1 5 2 4 4]
- **Fitness score:** a better fitness score means higher chance of being chosen to reproduce
- **Crossover:** a random point in the gene of a parent
- **Elitism:** a percentage of the previous generation’s most suitable (elite) members can be included in the next generation
- **Mutation:** the probability of a gene to mutate (i.e., change to random value)

#### Steps followed by the algorithm
- Initialize a random population
- Slice the population to include the most suitable members (those with the highest fitness score) [parents pool]
- In each generation, parents generate equal number of children based on their fitness score
- The population is sliced again to include the most suitable members (the number of members is fixed)
- The final population becomes the next population of parents and the loop continues if no solution is found

#### Final notes
1. Some techniques are used to increase the success rate of the algorithm, such as changing the mutation_rate, the elitism_factor and appending random members to the population, every x generations.
2. The initial values of the variables initial_population_size, number_of_parents, mutation_rate, max_generations and elitism_factor can be changed to alter the success rate and/or execution time.

<br>

## Example
How many queens? (4-100)\
10\
iteration 1: evaluation = 33.0\
iteration 2: evaluation = 39.0\
iteration 3: evaluation = 39.0\
iteration 4: evaluation = 39.0\
iteration 5: evaluation = 39.0\
iteration 6: evaluation = 39.0\
iteration 7: evaluation = 39.0\
iteration 8: evaluation = 39.0\
iteration 9: evaluation = 39.0\
iteration 10: evaluation = 40.0\
iteration 11: evaluation = 40.0\
iteration 12: evaluation = 40.0\
iteration 13: evaluation = 40.0\
iteration 14: evaluation = 40.0\
iteration 15: evaluation = 40.0\
iteration 16: evaluation = 40.0\
iteration 17: evaluation = 40.0\
iteration 18: evaluation = 40.0\
iteration 19: evaluation = 40.0\
iteration 20: evaluation = 40.0\
iteration 21: evaluation = 40.0\
Solved puzzle!\
Final state is:  

. . . . . . q .  . .\
. . . . q .  . . . .\
. . . . . . . q .  .\
q .  . . . . . . . .\
. . . . . . . . q . \
. . . q .  . . . . .\
. q .  . . . . . . .\
. . . . . . . . . q\
. . q .  . . . . . .\
. . . . . q .  . . .  

Process finished with exit code 0  

<br>
