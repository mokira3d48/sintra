# SinTra
This project is a python library that I was programming for data extraction with preprocessing from
different data sources (Website, audio, video, Map,etc...).

<br/>

## Installation et configuration

### Install python3 
```sh
sudo apt install python3
sudo apt install python3-pip
```
You have to make sure of the version of python that is installed. The version of python
used is `python 3.9.12`. You can also use version `3.8`.


### Install venv
```sh
sudo apt install python3-venv
```
OU
```sh
sudo pip3 install virtualenv
```

### Create virtual environment
```sh
python3 -m venv env
```
OU
```sh
virtualenv env -p python3
```

### Lauch environment
```sh
source env/bin/activate
```

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
You can use the command line interface to test the functions of the package or 
for other personal use, or use the python programming interface 
to integrate its features in your python projects.

### Command line interface
The following command displays the help on the available options.

```sh
python main.py --help
```

Display:

```
usage: main.py [-h] [--lev LEV] [--sen SEN] [--lang LANG] name url

positional arguments:
  name         Option name.
  url          URL of WEB page that you want scrap.

optional arguments:
  -h, --help   show this help message and exit
  --lev LEV    Set the navigation level. Default value is 0.
  --sen SEN    Set the keyword extractor sensibility. Default set to 4.
  --lang LANG  Select a language.
```

For example: 
- You want to extract the keywords from a web page :

```
python main.py getkw https://beautiful-soup-4.readthedocs.io/en/latest/
```

This command give :

```
[ INFO ]  Navigation level : 0
[ INFO ]  Navigation to https://beautiful-soup-4.readthedocs.io/en/latest/ ...
[ OK ]    STATUS CODE - 200 | https://beautiful-soup-4.readthedocs.io/en/latest/ is scrapped.

[ INFO ]  -> Language set to Lang.EN
[ INFO ]  -> Sensibility set to 4
[ INFO ]  Keyword extracting ... 
[ SUCC ]  9 keywords found!

   INDEX	                        KEYWORDS	     OCC
       1	                             tag	     273
       2	                            soup	     202
       3	                       beautiful	     157
       4	                  beautiful soup	     148
       5	                        document	     127
       6	                            stre	      96
       7	                            html	      86
       8	                          parser	      81
       9	                       attribute	      69
```

