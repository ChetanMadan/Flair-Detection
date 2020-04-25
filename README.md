# Reddit Flair Detectin  

### Steps to reproduce: 

1. Install requirements by running 

```python
pip install -r requirements.txt
```

2. Run the following jupyter notebooks present inside the Notebooks folder in the same order: 

- Data Gathering (Add credentials in cell 2 (Reddit agent) before running) 
- EDA Analysis
- Flair Detection

3. Go to folder app 

4. Run the flask application: 

Open terminal and execute the following commands: 

```
export FLASK_APP=main.py
flask run
```