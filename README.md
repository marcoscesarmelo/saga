# SAGA Transfer Service

# What is it?
Imagine a scenario whose we have 2 services, with its own database and each one has one purpose. 
One service only take money from an origin account. Other, only provide money to the second account.
They don't do the opposite task. Even only take money, or provide it.

# How to synchronize an amount transfer?
## In order to mantain integrity and data for those services, We've developed a third service called transfer_service.
```
As a customer
I want to take money from my account
So that, my amount money will be less than before
```
```
As a customer
I want to receive money to my account
So that, my amount money will be more than before
```
```
As a customer
I want to get my amount money updated after every transaction
So that, every channel will have the same information
```
The solution is shown on image below:

<img src="https://github.com/marcoscesarmelo/saga/blob/main/images/saga-transfer.jpg"/>

# How those services were developed?
3 Restful API's, were made to ilustrate this scenario. Tools used to provide this are: 

### What do I need to run those services locally?
* [Python](https://www.python.org) Python Language
* [SQLite](https://www.sqlite.org) - Database SQLite used to ilustrate
* Python libraries like Flask,  sqlite, requests and json (execute , for example, pip install command).


## About the Autor:
[Marcos Cesar de Oliveira Melo](https://www.linkedin.com/in/marcoscesarmelo/)

