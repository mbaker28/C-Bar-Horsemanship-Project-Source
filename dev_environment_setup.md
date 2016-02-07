# Setting up your local development environment
__Notes:__
* Replace `{Path to repository}` with the full path to your repository as
    applicable on each system.
* Replace `{Username}` with your local Windows or Linux user name.
* Potential issue: https://github.com/PyMySQL/mysqlclient-python/issues/54

## Under Windows
Tested on Windows 8.1, but should work with other versions.

1) Uninstall any other Python versions. Open the programs and features section
of the control panel, search for "python" and uninstall each version
individually.

2) Download and install [Python 3.5.1](https://www.python.org/ftp/python/3.5.1/python-3.5.1-amd64.exe).
__Make sure "Add Python 3.5 to PATH" is checked.__ You may need to run the
installer as an administrator. By default Python installs to
```
\Users\{Username}\AppData\Local\Programs\Python\Python35
```

3) Open up an admin command prompt (`windows-x`) and run the following:
```bash
python
```
to verify python installed correctly. You should see "Python 3.5.1 [......]".
Hit `control-c` to exit the Python prompt.

4) __Steps 4-6 may be unnecessary.__ Try them if you cannot get the `pip
install` step to work. Open powershell (windows menu -> type "powershell") and
run the following:
```bash
Start-Process powershell -Verb runAs
```

5) In the new window run (type `Y` or `Yes` at the prompt):
```bash
Set-ExecutionPolicy RemoteSigned
```

6) Close the two powershell windows.

7) Update pip:
```bash
python -m pip install --upgrade pip
```

8) Install virtualenv.
```bash
python -m pip install virtualenv
```
9) Navigate to the top level folder of this repository in the admin command
    prompt.

10) Create the virtual environment:
```bash
python -m virtualenv env
```
__Note:__ This will most likely fail if your repository pathname contains spaces
or other special characters.

11) Activate the virtual environment:
```bash
env\Scripts\activate
```
If it was successful you will see `(env)` at the beginning of your command prompt.

12) Install Django v1.9.1 (this may take some time):
```bash
python -m pip install django==1.9.1
```

13) Install mysqlclient (Django library):
```bash
python -m pip install mysqlclient-1.3.7-cp35-none-win_amd64.whl
```

14) [Download](http://downloads.mysql.com/archives/get/file/mysql-5.5.44-winx64.msi)
and install MySQL Community 5.5.44 server. Select "Standard Configuration" when
prompted. Check "Include Bin Directory in Widows PATH". Set the root password to
`localtestpass`. The rest of the default settings should be fine.

15) Open the MySQL Command Line Client (windows key -> 'mysql' -> click name),
enter the password you set in the last step, and run:
```SQL
CREATE DATABASE cbar_test;
```
To verify it created the DB correctly you can run:
```SQL
SHOW DATABASES;
```

16) Run the test server:
```bash
cd cb*
python manage.py runserver --settings cb_info_db.settings_dev
```

## Under Linux

__WARNING: Outdated__

1) Clone the repository from Bitbucket.

2) Create a an empty folder name `env` in the top level of the git repository to
 store the virtual environment in. __The `env` folder should never be pushed to
 Bitbucket__ because it is specific to each machine.

3) Install python 3.5.1
```bash
$ sudo apt-get install python3
```

4) Install virtualenv
```bash
$ virtualenv --python=python3.5 {path to repository}/env
```

4) Activate the virtual environment.
__You will need to do this step every time you start working.__
```bash
$ source {path to repository}/env/bin/activate
```

5) Install Django.
```bash
$ pip install django==1.9.1
```

Test the setup. Navigate to the folder that contains `manage.py`
(this should be `{path to repository}/cb_info_db/`) Run:
```bash
$ python manage.py runserver --settings cb_info_db.settings_dev
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
Try `pip install mysqlclient==1.3.7` again.
If it fails and gives the
`error: command 'x86_64-linux-gnu-gcc' failed with exit status 1`,
do this and then try again:
```bash
$ sudo apt-get install python3.5-dev
```
