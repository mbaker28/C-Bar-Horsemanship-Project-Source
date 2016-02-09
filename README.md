# C-Bar Information Database - Source Code
This repository contains the source code for the C-Bar Information Database
 Project.

## Setting up Development Environment
Instructions [here](SETUP.md).

## Starting a Development Session
#### Windows

1) Open a command prompt to the top level of the repository. Run:
```bash
env\scripts\activate
```

2) Run the development server. Navigate to the `cb_info_db` folder and run:
```bash
python manage.py runserver --settings cb_info_db.settings_dev
```

3) Do your develop. Hail Python!

If you need to make changes using manage.py, run them in the command prompt like
 so:
```bash
python manage.py
```
If you are having problems, make sure you are in the root folder of the
repository and `(env)` is at the start of your command prompt. If not, redo step
1 and then try again.

## Testing user

This account is needed to access any portion of the DB system through the web
 browser while in development.

* Username: test
* Password: inw@EngMZUz!EG3hQC^P5!Z4t$tQm9gD

## Git Contribution Workflow
This is the workflow for making a contribution to this Git repository.

1. Checkout the ```master``` branch.
2. Pull changes from ```master``` (if any).
3. Create a new branch from ```master```. Name it
 ```issue-###-name-of-the-issue```. For example: ```issue-3-fix-form-overlap-in-internet-explorer```.
4. Checkout this branch.
5. Make some changes.
6. Commit the changes to this branch. Start each commit message with
 ```[Re #{issue number}]```. For example, ```[Re #1]```.
7. Repeat steps 5&6 until the issue should be resolved.
8. Pull changes on the ```master``` branch (if any).
9. Merge the ```master``` branch onto the ```issue-###-...``` branch.
10. Make sure that everything is still functioning as expected.
11. Push the ```issue-###-...``` branch to the repository.
12. Create a pull request with the same name as this branch. Add at least one
 team member as a reviewer (typically Michael).
13. The pull request should then be reviewed by at least one other team member
 and approved.
14. Once the pull request is approved, Michael will merge the pull request
 onto master.

### Branches

* `master` is the main working development branch. Any pushes to the server
 will be made from this branch.
* `Issue-{number}-...` branches are branches containing new or modified code
 that address the relevant issue {number}.
