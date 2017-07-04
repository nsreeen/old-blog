title: virtualenvs
date: 2017-05-29 12:00:00
published: false
type: notes

* to set python3 as the defualt in the env:
virtualenv --python=python3

* make sure there are no spaces anywhere in the path

* install requirements in one go:
pip install -r requirements.txt

* to make globally installed packages inaccessible:
virtualenv --no-site-packages --python=python3 venv

