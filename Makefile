PYTHON      := python3
SRC_DIR     := src
MAIN        := $(SRC_DIR)/a_maze_ing.py
CONFIG      := config.txt

.PHONY: install run debug clean fclean re lint lint-strict

install:
	poetry install

run:
	cd $(SRC_DIR) && $(PYTHON) a_maze_ing.py ../$(CONFIG)

debug:
	cd $(SRC_DIR) && $(PYTHON) -m pdb a_maze_ing.py ../$(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

fclean: clean
	rm -f maze.txt

re: fclean run

lint:
	flake8 . --exclude=venv,.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude=venv --exclude=.venv

lint-strict:
	flake8 . --exclude=venv,.venv
	mypy . --strict --exclude=venv --exclude=.venv
