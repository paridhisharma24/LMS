<<<<<<< HEAD
# Learning Management System
=======
# Learning Management system
>>>>>>> origin/db-update


## Description
The Learning Management System is an EdTech application that helps in delivering and managing the course smoothly. The application helps the educator in conducting the course by providing interfaces for sharing the material for the courses, assignments. The main aim of this application is to increase the interaction between students and teachers through discussion forums, bots, and so on. This portal will also help the users to keep a track of deadlines and the upcoming sessions which will boost the flexibility of the work process and work management. In the current circumstances where the learning is shifted to remote mode, this application will provide a smoother experience to the educators and the educates by replicating the actual offline learning environment.


## Table of Content
1. [ How to download ](#run)
2. [ Set up  a Virtual Environment ](#venv)
3. [ Install dependencies ](#usage)
<<<<<<< HEAD
4. [ Update flask-login ](#update)
5. [ Run the website ](#start)
=======
4. [ Run the website ](#start)
>>>>>>> origin/db-update

<a name="run"></a>
## How to download
1. Make sure you have Git properly setup using your GitHub account.
2. Run the following command in terminal to clone this repository in your device locally:
```
<<<<<<< HEAD
git clone https://github.com/paridhisharma24/LMS.git
=======
git clone https://github.com/<your_username>/LMS.git
>>>>>>> origin/db-update
```

<a name="venv"></a>
## Set up  a Virtual Environment
1. Make sure you are in the same directory in which the project was cloned (for simplicity).
2. Install pip (python 3):
```
sudo apt update
```
```
sudo apt install python3-pip
```
<<<<<<< HEAD
3. Install virtual environment package:
```
pip install virtualenv
```
4. Create virtual environment (<venv_name> is user specifiedname):
```
virtualenv <venv_name>
```
4. Activate the virtual environment (make sure you are in the same directory in which venv is created):
```
for Mac OS/ Linux:
    source <venv_name>/bin/activate
for Windows:
    <venv_name>\Scripts\activate
=======
3. Setup virtual environment:
```
pip install <venv_name>
```
4. Activate the virtual environment (make sure you are in the same directory in which venv is created):
```
source <venv_name>/bin/activate
>>>>>>> origin/db-update
```

<a name="Install dependencies"></a>
## Install dependencies
1. To make sure all the packages are installed properly and up-to-date with this project, run:
```
pip install -r requirements.txt
```

<<<<<<< HEAD
<a name="update"></a>
## Update flask-login
1. Go to:
```
<venv_name>/bin/flask_login
```
2. Open the file _mixins.py_
3. In the function *_get_id_ of _mixins.py_*, update return statement:
```
from:
    return self.id
to:
    return self.user_id
```


<a name="start"></a>
## Run the Website
1. In the terminal, run:
=======
<a name="start"></a>
## Run the Website
1. In the terminal, type:
>>>>>>> origin/db-update
```
python3 main.py
```
