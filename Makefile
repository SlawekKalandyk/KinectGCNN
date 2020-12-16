PIPENV=python -m pipenv

.PHONY: install
install:
	$(PIPENV) install
	$(PIPENV) run pip install PyKinect2-master.zip

.PHONY: run
run:
	$(PIPENV) run python -m app