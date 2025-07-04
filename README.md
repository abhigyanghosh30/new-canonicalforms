# 2025 Rewrite of forms.canonical.com

### Rationale for the rewrite
This rewrite is because forms.canonical.com was unmaintained for a long time and the design looked outdated. 
With the switch to charms, it became clear that charming such an old application would be really time consuming and that time could actually be spent rewriting the code. 
It was decided to rewrite the website in Flask instead of Django

### Running the website
1. Create a new virtualenv for python and activate it
```
python -m venv .venv
source .venv/bin/activate
```
2. Install required packages
```
pip install -r requirements.txt
```
3. 
To run the website:
```
flask run -p 8050 --debug
```
