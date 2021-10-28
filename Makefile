ENV = env
PYTHON = python3

run:
	$(PYTHON) src/features/preprocessing.py
	$(PYTHON) src/all_distributions.py
	$(PYTHON) src/all_exchanges.py
	$(PYTHON) src/visualization/plot_metric.py
	$(PYTHON) src/visualization/plot_grid.py
