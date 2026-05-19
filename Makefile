PYTHON      := python3
SRC_DIR     := src
PACKAGE_DIR := mazegen_maroard_almanier
MAIN        := $(SRC_DIR)/a_maze_ing.py
CONFIG      := config.txt

.PHONY: install run debug build clean fclean re lint lint-strict

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

run:
	cd $(SRC_DIR) && $(PYTHON) a_maze_ing.py ../$(CONFIG)

debug:
	cd $(SRC_DIR) && $(PYTHON) -m pdb a_maze_ing.py ../$(CONFIG)

build:
	$(PYTHON) -m build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf dist

fclean: clean
	rm -f maze.txt

re: fclean run

lint:
	cd $(SRC_DIR) && $(PYTHON) -m flake8 .
	cd $(SRC_DIR) && $(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

	$(PYTHON) -m flake8 $(PACKAGE_DIR)
	$(PYTHON) -m mypy $(PACKAGE_DIR) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	cd $(SRC_DIR) && $(PYTHON) -m flake8 .
	cd $(SRC_DIR) && $(PYTHON) -m mypy . --strict

	$(PYTHON) -m flake8 $(PACKAGE_DIR)
	$(PYTHON) -m mypy $(PACKAGE_DIR) --strict
