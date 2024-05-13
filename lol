c for file in puzzles/valid/*; do
  echo "$file"
  p npuzzle.py --file "$file" --line-by-line --solver greedy --heuristic manhattan
done