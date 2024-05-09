help:
	@python npuzzle.py --help

test:
	pytest -vv

clean:
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@rm -rf .pytest_cache */.pytest_cache */*.pytest_cache
	@rm -rf .coverage test_gen.txt

loc:
	@find . -name '*.py' | sort | xargs wc -l
