END := \033[0m
GREEN := \033[1m\033[32m

all:
	-@$(MAKE) --no-print-directory clean > /dev/null
	-@$(MAKE) --no-print-directory test
	-@$(MAKE) --no-print-directory clean > /dev/null

test:
	pytest -vv

help:
	@python npuzzle_solve.py || true

clean:
	rm -rf __pycache__ .pytest_cache .coverage test_gen.txt