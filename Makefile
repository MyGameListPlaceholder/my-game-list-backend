# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "MyGameList Makefile"
	@echo "run - Start the application on the default port."
	@echo "fresh_run - Use for the first start of the application. It collects the static files,"
	@echo "            runs the migrations, prompts for superuser creation, and at the end runs the application."
	@echo "check - Check the correctness of code with black formatter and flake8."

run:
	my-game-list-manage.py runserver

fresh_run:
	my-game-list-manage.py collectstatic
	my-game-list-manage.py migrate
	my-game-list-manage.py createsuperuser
	my-game-list-manage.py runserver

check:
	black .
	flake8

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY: help run fresh_run check
