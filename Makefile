env:
	poetry install
	pre-commit install


shell:
	poetry shell || source ~/.bash_profile


lint:
	pre-commit run --all-files
