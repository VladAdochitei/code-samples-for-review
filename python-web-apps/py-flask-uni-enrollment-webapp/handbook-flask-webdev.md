# Web Development Handbook - Python-Flask
Python Flask Flramework full-stack web development handbook that briefly covers some topics related to the current project

---------------------------------------------------

## Contents
- [0. Virtual Environment](#0-virtual-environment)
    - [0.1. Create the virtual environment](#01-create-the-virtual-environment)
    - [0.2. Activate the virtual environment](#02-activate-the-virtual-environment)
    - [0.3. deactivate the virtual environment](#03-deactivate-the-virtual-environment)
- [1. Pip](#1-pip)
    - [1.1. Install packages](#11-install-packages)
    - [1.2. Freeze the requirements](#12-freeze-the-requirements)
    - [1.3. Install the requirements](#13-install-the-requirements)
- [2. Request object](#2-request-object)
    - [2.1. Accessing query string (GET)](#21-accessing-query-string-get)
    - [2.2. Accessing form data (POST)](#22-accessing-form-data-post)
- [3. Response Object](#3-response-object)
- [4. To show content twice](#4-to-show-content-twice)
- [5. MongoDB Basics](#5-mongodb-basics) !!!!!!!!!!!!!!!!!!!!!!!!!!!!! Start from here and create a new handbook in the `handbook-library repo: handbook-mongodb`


---------------------------------------------------

<br>

## 0. Virtual Environment

### 0.1. Create the virtual environment

```sh
python -m venv virtenv
```

### 0.2. Activate the virtual environment

```sh
source ./virtenv/bin/activate
```

### 0.3. Deactivate the virtual environment

```sh
deactivate
```

<br>

## 1. Pip

### 1.1. Install packages

```sh
pip install PACKAGE_NAME
```

### 1.2. Freeze the requirements
Before running thi scommand make sure that the virtual environment is activated.

```sh
pip freeze > requirements.txt
```

### 1.3. Install the requirements 

```sh
pip install -r requirements.txt
```

<br>

## 2. Request Object
Can be used to access data.

### 2.1. Accessing Query String (GET)

```py
request.args.get(<field_name>)
request.args[<field_name>]
```

### 2.2. accessing Form Data (POST)

```py
request.form.get(<field_name>)
request.form[<field_name>]
```

<br>

## 3. Response object
Usually used for creating APIs. 

Flask has a built in class called the response object `flask.Response(...)`

```py
class flask.Response(
    response = None,
    status = None,
    headers = None, 
    mimetype = None, 
    content_type = None,
    direct_passthrough = False
)
```

For this, the most common parameters are:
- `response`
- `mimteype`
- `content_type`

<br>

## 4. To show content twice

```jinja2
{{ self.content() }}
```

<br>

## 5. MongoDB Basics

### 5.1. Database commands 
Show databases:

```
show dbs
```

Create/Use database:

```
use DB_NAME
```

Delete a database

```
db.dropDatabase()
```

### 5.2. Collection commands
Create collection in the database:

```
db.createCollection("COLLECTION_NAME")
```

List collections in a database:

```
db.getCollectionNames()

show collections
```

Delete collection record:

```
db.COLLECTION.drop()
```

Insert data in a database collection:

```
db.<COLLECTION>.insert({...})
```

Insert more data at once in a database collection:

```
db.<COLLECTION>.insertMany({...})
```

### 5.3. Inserting JSON data using the `mongoimport.exe`:
To import data into a database from a json file:

```sh
mongoimport --db DB --collection COLLECTION --file FILE
```

or

```sh
mongoimport -d DB -c COLLECTION --file FILE
```

Commands to import the data:

```sh
mongoimport --jsonArray --db Enrollment_Web_App_Db --collection user --upsertFields user_id  --file ./models/users.json 
mongoimport --jsonArray --db Enrollment_Web_App_Db --collection courses --upsertFields courceID  --file ./models/courses.json 
```

If it fails to import, adding this flag `--jsonArray` immediately after the `mongoimport` might work.
Another flags that will work are:
- `--jsonArray`: because in our case the data is structured in a JSON arrat `[{json}]`
- `--upsertFields`: By default, Mongo will look for the `_id` field, but if you have achieved uniqueness through other fields you will have to pass them with this command. `--upsertFields id,name` it supports more parameters spearated with a comma

### 5.4. Documents
Remove a document from the database:

```
db.collection.remove(<query>)

# to delete all documents in collection

db.collection.remove({})
```

<br>

## 6. HTTPY
HTTPY is a tool that can be used to create and test apis