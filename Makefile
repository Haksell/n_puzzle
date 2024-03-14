END := \033[0m
GREEN := \033[1m\033[32m

all:
	-@$(MAKE) --no-print-directory clean > /dev/null
	-@$(MAKE) --no-print-directory test
	-@$(MAKE) --no-print-directory clean > /dev/null

test:
	pytest -rA -vv

run:
	@# TODO: accept argument
	@python npuzzle_solve.py puzzles/valid/subject3.txt

clean:
	rm -rf __pycache__ .pytest_cache .coverage