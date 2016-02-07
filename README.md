# C-Bar Information Database - Source Code
This repository contains the code for the C-Bar Information Database Project.

## Setting up Development Environment
Instructions [here](dev_environment_setup.md).

## Starting a Development Session
#### Windows

1. Open a command prompt to the top level of the repository. Run:
```bash
env\scripts\activate
```

2. Run the development server. Navigate to the `cb_info_db` folder and run:
```bash
python manage.py runserver --settings cb_info_db.settings_dev
```

3. Do your develop.

If you need to make changes using manage.py, run them in the command prompt like so:
```bash
python manage.py
```
If you are having problems, make sure you are in the root folder of the repository and `(env)` is at the start of your command prompt. If not, redo step 1 and then try again.

## Testing user

This account is needed to access any portion of the DB system through the web browser while in development.

* Username: test
* Password: inw@EngMZUz!EG3hQC^P5!Z4t$tQm9gD

## Branches

* `master` is the main working development branch.
* `DEPLOYMENT-{year}-{month}-{day}-...` branches correspond to a specific deployment push to the Dreamhost server that started on the given day.
* `Issue-{number}-...` branches are branches containing new or modified code that address the relevant issue {number}.
