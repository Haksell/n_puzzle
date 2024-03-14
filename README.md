# n_puzzle

## mandatory

-   [ ] You must provide a Makefile with the usual rules.
-   [ ] Implement the A\* search algorithm (or one of its variants, you’re free to choose) to solve an N-puzzle
-   [ ] You have to manage various puzzle sizes (3, 4, 5, 17, etc ...). The higher your program can go without dying a horrible, horrible death, the better.
-   [ ] You have to manage both randomly determined states (of your own generation of course), and input files that specify a starting board, the format of which is described in the appendix.
-   [ ] The cost associated with each transition is always 1.
-   [ ] The user must be able to choose between at LEAST 3 (relevant) heuristic functions. The Manhattan-distance heuristic is mandatory, the other two are up to you. By "relevant" we mean they must be admissible (Read up on what this means) and they must be something other than " just return a random value because #YOLO".
-   [ ] Show total number of states ever selected in the "opened" set (complexity in time)
-   [ ] Show maximum number of states ever represented in memory at the same time during the search (complexity in size)
-   [ ] Show number of moves required to transition from the initial state to the final state, according to the search
-   [ ] Show the ordered sequence of states that make up the solution, according to the search
-   [ ] The puzzle may be unsolvable, in which case you have to inform the user and exit

## bonus

-   [ ] For the bonus part you can configure the appropriate g(x) and h(x) functions to run both the uniform-cost and greedy searches. Execute with the same output (Of course, the solution may be different. Read up on why, that’s the point.)
-   [ ] Normal and Snail mode

## misc

-   bfs solver
-   iterated dfs solver
-   A\* solver
-   row by row solver
-   better solvers
-   recode in Rust?
-   graphical visualization

## resources

-   https://en.wikipedia.org/wiki/A*_search_algorithm
-   https://en.wikipedia.org/wiki/Admissible_heuristic
