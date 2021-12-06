env:
	poetry install
	pre-commit install


shell:
	poetry shell || source ~/.bash_profile || source ~/.bashrc


lint:
	pre-commit run --all-files
