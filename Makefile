.PHONY: install
install:
	pipenv install
	pipenv run pip install PyKinect2-master.zip

.PHONY: run
run:
	pipenv run py -m app