# C-Bar Information Database - SOURCE CODE
This repository contains the source code for the C-Bar Information Database
 Project.

## Starting a Development Session (Windows)

1) Open a command prompt to the top level of the repository. Run:
```bash
env\scripts\activate
```

2) Run the development server. Navigate to the `cb_info_db` folder and run:
```bash
python manage.py runserver --settings cb_info_db.settings_dev
```
This will allow you to test on the machine the server is running on by visiting
 `localhost:8000` in the browser. If you want to access the development server
 on a different device on the local network (i.e to test on a tablet or phone),
 run this instead:
```bash
python manage.py runserver --settings cb_info_db.settings_dev 0.0.0.0:8000
```
Then visit `{your_computers_ip_number}:8000`
 (for example `172.16.104.114:8000`) in a web browser on the other device. You
 can find your IP address by running `ipconfig`. Keep in mind this will be
 accessible to every device on the local network.

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

This account is needed to access any portion of the
[db.cbarhorsemanship.org](http://db.cbarhorsemanship.org) while in development.

* Username: test
* Password: inw@EngMZUz!EG3hQC^P5!Z4t$tQm9gD

## Coding Style
[This document](CODING_STYLE.md) outlines guidelines to follow regarding coding
 styles used. It includes how we will do variable naming, use whitespace, etc.

## Setting up Development Environment
Instructions [here](SETUP.md).

## Things you should probably have installed

* [SmartGit](http://www.syntevo.com/smartgit/): Git client.
* [Atom](https://atom.io/): Text editor; I would suggest the following
 extensions: `autocomplete-python`, `hard-wrap`, `minimap`, `pdf-view`,
 `pigments`, `python-tools`, `script`, `terminal-plus`, and `multi-cursor`.
* [Slack](http://cbar-capstone.slack.com)

## Tests
* [Shippable](https://app.shippable.com/): Continuous Integration provider.
 Essentially it runs the tests every time a commit is pushed to the repository.

## Git
This is the workflow for making a contribution to this Git repository.

1. Checkout the ```master``` branch.
2. Pull changes from ```master``` (if any).
3. Create a new branch from ```master```. Name it
```issue-###-name-of-the-issue```. For example:
```issue-3-fix-form-overlap-in-internet-explorer```.
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

### Issues

* [Linking Issues with Commit Messages](https://confluence.atlassian.com/bitbucket/resolve-issues-automatically-when-users-push-code-221451126.html#Resolveissuesautomaticallywhenuserspushcode-IncludingIssuesinaCommitMessage)
