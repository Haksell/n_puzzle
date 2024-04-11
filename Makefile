MAIN := src/npuzzle_solve.py
END := \033[0m
GREEN := \033[1m\033[32m

help:
	@python $(MAIN) --help

all:
	-@$(MAKE) --no-print-directory clean > /dev/null
	-@$(MAKE) --no-print-directory test
	-@$(MAKE) --no-print-directory clean > /dev/null

test:
	pytest -vv

clean:
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@rm -rf .pytest_cache */.pytest_cache */*.pytest_cache
	@rm -rf .coverage test_gen.txt