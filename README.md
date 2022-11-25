# KYX0
Program of keywords extraction

<br>

## Python version

```sh
python --version
```

Show :

```
Python 3.8.10
```


## Installing of dependancies
1. Install the requirements.txt content.

```sh
pip install -r requirements.txt

```

2. Install FR and EN pipeline for spacy module used.

```sh
python -m spacy download en_core_web_md
python -m spacy download fr_core_news_md
```

## Using

```sh
python main.py getkw https://your_url_here
```

