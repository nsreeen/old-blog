title: heroku
date: 2017-06-10 12:00:00
published: false
type: notes

# Steps to publishing a heroku app
Some things you need:
- requirements.txt
- Procfile
- runtime.text
- the port to be set


## 1) Make a virtualenv and generate a requirements.txt file

This is important because you know everything works in a controlled environment you can replicate on the heroku servers
(Also, you can set the version of python you want to use in a virtualenv)

``` 
virtualenv venv
source venv/bin/activate
python app.py 
```
Check it works when you run the app (or whatever the runnable script is called)
Install whatever libraries you need in the virtualenv to make it work
Now you can easily make the requirements.txt file:

```
pip freeze > requirements.txt
```

#2) Make a Procfile

The Procfile should be one line:

```
web: python app.py
```
web: because it's a web app, followed by the command you use to run it from your terminal ('python app.py')

(should it end with  ${PORT} ?)


#3)Make runtime.txt

The runtime file should have the version of python you are using


#4) Set the port!
 

```
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```
