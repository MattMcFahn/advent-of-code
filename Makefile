

env:
	poetry install
	pre-commit install


shell:
	poetry shell || source ~/.bash_profile


pre-commit:
	pre-commit run --all-files
