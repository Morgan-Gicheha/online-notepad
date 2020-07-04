# Notepad Application

This a python/flask application that basically stores your todo lists.login is required to access this applications functionality. To view the final product [click here](https://free-online-notepad.herokuapp.com/login)

This application has the following code functionalites..

1.User registration and login 

2.Creating todo(s)

3.Updating the stored to do

4.Deleting of the todo

5.Database sqlalchemy

6.UI is done with bootstrap


Installation 
=====================

This is an overview of Markdown's syntax.  For more information, visit the [Ma

It is a requirement that you have Python3 installed in your computer.

1.clone the project

```bash
git clone https://github.com/codeGiche/online-notepad.git
```
2.Create a virtual environment
```bash
python -m venv venv
```
3.Activate the virtual environment
```bash
Source venv/Scripts/activate
```
4. Install requirements
```bash
pip install -r reqiurements.txt
```


Using activate login with github
=====================


In order to activate the Third party authentication with github, you  atleast have to own a github account.

## steps to activation of 3rd party auth
  1. Login to github
  2. Navigate to the settings option
  
      ![](.\images\git.png)

  3. Navigate to the developer settings


      ![](.\images\developer_set.png)


  3. Navigate to Aouth apps and click New Oauth App

      ![](.\images\aouth.png)


4. Fill the relevant [view github docs on Oauth Apps](https://developer.github.com/apps/building-oauth-apps/)


5. Get the github keys . client ID and Client Secret
![](.\images\get_keys.png)

   Working Github Keys
   =====================
   1. Inside the free-online-notepad navitage to configs/auth_config.py
   ![](.\images\git_keys.jpg)

   2. paste the Client ID and Client Secret to GITHUB_CONSUMER_KEY and GITHUB_CONSUMER_SECRET respectively



Running Application
=====================
1.Set flask_app 
```bash
export FLASK_APP=main.py
```
2.Run flask app

BEFORE running the application , make sure u insert the relevant database URI's .

```bash
flask run
```

## Usage
To view the apps documentation, navigate to your localhost(browser)
```python
127.0.0.1/
```

## Contributing
Feel free to make it better [fork me](https://github.com/codeGiche/online-notepad.git)

