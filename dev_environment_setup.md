# Setting up your local development environment
__Note:__ Replace `{Path to repository}` with the full path to your repository as applicable on each system.

## Under Linux

1. Clone the repository from Bitbucket.

2. Create a an empty folder name `env` in the top level of the git repository to store the virtual environment in. __The `env` folder should never be pushed to Bitbucket__ because it is specific to each machine.

3. Install python 3.5.1
```bash
$ sudo apt-get install python3
```

4. Install virtualenv
```bash
$ virtualenv --python=python3.5 {path to repository}/env
```

4. Activate the virtual environment. __You will need to do this step every time you start working.__
```bash
$ source {path to repository}/env/bin/activate
```

5. Install Django.
```bash
$ pip install django==1.9.1
```

Test the setup. Navigate to the folder that contains `manage.py` (this should be `{path to repository}/cb_info_db/`) Run:
```bash
$ python3 manage.py runserver --settings cb_info_db.settings_dev
```

You should see something like this (text color will most likely be different):

```bash
Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

February 05, 2016 - 21:23:32
Django version 1.9.1, using settings 'cb_info_db.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

__If you get errors, try this:__
```bash
$ pip install mysqlclient==1.3.7
```
If the terminal returns `OSError: mysql_config not found`, run:
```bash
$ sudo apt-get install libmysqlclient-dev
```
Try `pip install mysqlclient==1.3.7` again. If it fails and gives the `error: command 'x86_64-linux-gnu-gcc' failed with exit status 1`, do this and then try again:
```bash
$ sudo apt-get install python3.5-dev
```
