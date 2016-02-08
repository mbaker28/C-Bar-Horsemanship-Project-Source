# Setting up your local development environment
__Notes:__

* Replace `{Path to repository}` with the full path to your repository as
    applicable on each system.
* Replace `{Username}` with your local Windows or Linux user name.
* Potential issue: https://github.com/PyMySQL/mysqlclient-python/issues/54

## Under Windows
Tested on Windows 8.1, but should work with other versions.

1) If you have not already, clone this repository. __Make sure there are no spaces or special characters in the path name.__

2) Create an empty folder name `env` in the top level of the git repository to
 store the virtual environment in. __The `env` folder should never be pushed to
 Bitbucket__ because it is specific to each machine.

3) Uninstall any other Python versions. Open the programs and features section
of the control panel, search for "python" and uninstall each version
individually.

4) Download and install [Python 3.5.1](https://www.python.org/ftp/python/3.5.1/python-3.5.1-amd64.exe).
__Make sure "Add Python 3.5 to PATH" is checked.__ You may need to run the
installer as an administrator. By default Python installs to
```
\Users\{Username}\AppData\Local\Programs\Python\Python35
```

5) Open up an admin command prompt (`windows-x`) and run the following:
```bash
python
```
to verify python installed correctly. You should see "Python 3.5.1 [......]".
Hit `control-z` and then `enter` to exit the Python prompt.

6) __Steps 4-6 may be unnecessary.__ Try them if you cannot get the `pip
install` step to work. Open powershell (windows menu -> type "powershell") and
run the following:
```bash
Start-Process powershell -Verb runAs
```

7) In the new window run (type `Y` or `Yes` at the prompt):
```bash
Set-ExecutionPolicy RemoteSigned
```

8) Close the two powershell windows.

9) Update pip:
```bash
python -m pip install --upgrade pip
```

10) Install virtualenv.
```bash
python -m pip install virtualenv
```
11) Navigate to the top level folder of this repository in the admin command
    prompt.

12) Create the virtual environment:
```bash
python -m virtualenv env
```
__Note:__ This will most likely fail if your repository pathname contains spaces
or other special characters.

13) Activate the virtual environment.
```bash
env\Scripts\activate
```
If it was successful you will see `(env)` at the beginning of your command prompt.

14) Install Django v1.9.1 (this may take some time):
```bash
python -m pip install django==1.9.1
```

15) Install mysqlclient (Django library):
```bash
python -m pip install mysqlclient-1.3.7-cp35-none-win_amd64.whl
```

16) [Download](http://downloads.mysql.com/archives/get/file/mysql-5.5.44-winx64.msi)
and install MySQL Community 5.5.44 server. Select "Standard Configuration" when
prompted. Check "Include Bin Directory in Widows PATH". Set the root password to
`localtestpass`. The rest of the default settings should be fine.

17) Open the MySQL Command Line Client (windows key -> 'mysql' -> click name),
enter the password you set in the last step, and run:
```SQL
CREATE DATABASE cbar_test;
```
To verify it created the DB correctly you can run:
```SQL
SHOW DATABASES;
```

18) Test the setup. Navigate to the folder that contains `manage.py`
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

## Under Linux

1) If you have not already, clone this repository. __Make sure there are no spaces or special characters in the path name.__

2) Create an empty folder name `env` in the top level of the git repository to
 store the virtual environment in. __The `env` folder should never be pushed to
 Bitbucket__ because it is specific to each machine.

3) Install python 3.5.1:
```bash
$ sudo apt-get install python3 && apt-get install python3.5-dev
```

4) Install virtualenv:
```bash
$ sudo pip install virtualenv
```

5) Create the virtual environment:
```bash
$ virtualenv --python=python3.5 {path to repository}/env
```

6) Activate the virtual environment.
```bash
$ source {path to repository}/env/bin/activate
```

7) Install Django:
```bash
$ pip install django==1.9.1
```

8) Install MySQL server. Unfortunately it's difficult to get a specific version on Linux. Try this first:
```bash
$ sudo apt-get install mysql-server-5.5
```
If that doesn't work, run this instead:
```bash
$ sudo apt-get install mysql-server
```
This will prompt you to set a password for the root MySQL user. Set it to `localtestpass`.

9) Start the MySQL server:
```bash
$ sudo /etc/init.d/mysql start
```

10) Open the MySQL Command Line Client:
```bash
$ mysql -h localhost -u root -p
```

11) Enter the password you set when you installed MySQL (`localtestpass`), and run:
```SQL
CREATE DATABASE cbar_test;
```
To verify it created the DB correctly you can run:
```SQL
SHOW DATABASES;
```
Hit `control-c` to exit the MySQL client.

13) Install components needed for MySql <-> Django integration:
```bash
$ sudo apt-get install libmysqlclient-dev
$ pip install mysqlclient==1.3.7
```

12) Test the setup. Navigate to the folder that contains `manage.py`
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
