# n_puzzle

## mandatory

-   [x] You must provide a Makefile with the usual rules.
-   [x] Implement the A\* search algorithm (or one of its variants, you’re free to choose) to solve an N-puzzle
-   [ ] You have to manage various puzzle sizes (3, 4, 5, 17, etc ...). The higher your program can go without dying a horrible, horrible death, the better.
-   [ ] You have to manage both randomly determined states (of your own generation of course), and input files that specify a starting board, the format of which is described in the appendix.
-   [x] The cost associated with each transition is always 1.
-   [x] The user must be able to choose between at LEAST 3 (relevant) heuristic functions. The Manhattan-distance heuristic is mandatory, the other two are up to you.
-   [ ] Show total number of states ever selected in the "opened" set (complexity in time)
-   [ ] Show maximum number of states ever represented in memory at the same time during the search (complexity in size)
-   [ ] Show number of moves required to transition from the initial state to the final state, according to the search
-   [x] Show the ordered sequence of states that make up the solution, according to the search
-   [x] The puzzle may be unsolvable, in which case you have to inform the user and exit

## bonus

-   [x] Configure g(x) and h(x) to run both the uniform-cost and greedy searches
-   [x] Visualizer
-   [ ] Rectangles from_file, solvable and unsolvable files
-   [ ] Normal and Snail mode

## solvers

-   [x] A\*
-   [x] Greedy Search
-   [x] Uniform Cost Search
-   [x] IDA\*
-   [ ] LPA\*
-   [ ] SMA\*
-   [ ] ID-Dual\* or Bi-directional A\*
-   [ ] JPS+
-   [ ] Row/Col solver (don't allow with pattern databases)
-   ... https://chat.openai.com/c/10a31ea2-f76b-49db-86f3-f3adaeb3e31e

## heuristics

-   [x] manhattan
-   [x] euclidean
-   [x] chebyshev
-   [x] manhattan with conflicts
-   [x] hamming
-   [x] inversion distance
-   [ ] walking distance
-   [ ] pattern databases

## resources

-   https://en.wikipedia.org/wiki/A*_search_algorithm
-   https://en.wikipedia.org/wiki/Iterative_deepening_A*
-   https://en.wikipedia.org/wiki/SMA*
-   https://en.wikipedia.org/wiki/Lifelong_Planning_A*
-   https://en.wikipedia.org/wiki/Heuristic_(computer_science)
-   https://en.wikipedia.org/wiki/Admissible_heuristic
-   https://en.wikipedia.org/wiki/Consistent_heuristic
-   https://michael.kim/blog/puzzle
-   https://medium.com/swlh/looking-into-k-puzzle-heuristics-6189318eaca2
-   https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/
-   https://algorithmsinsight.wordpress.com/graph-theory-2/implementing-bfs-for-pattern-database/
-   https://laconicml.com/simplified-memory-bounded-a-star/
-   https://mice.cs.columbia.edu/getTechreport.php?techreportID=1026&format=pdf&
-   https://www.lamsade.dauphine.fr/~cazenave/papers/SOAPH.pdf
-   https://cdn.aaai.org/AAAI/1996/AAAI96-178.pdf
-   https://www.educative.io/answers/what-is-uniform-cost-search
-   https://www.scaler.com/topics/uniform-cost-search/
-   https://www.javatpoint.com/ai-uninformed-search-algorithms
-   https://www.geeksforgeeks.org/uniform-cost-search-dijkstra-for-large-graphs/
