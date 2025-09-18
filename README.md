# README

## Setup

For development environment setup, project commands, and usage instructions, please see [HELP.md](HELP.md).

## The test

### Description Of Problem

At Elixir we often have to work with third party apis and ingest data into our system, we write bespoke programs that we call `biz_rules` to perform this integration. This test is a scale model of the sort of work we do quite frequently and is quite reflective of what a typical day might look like, the system uses django rest framework to create a viewable api in the browser.

It is designed as a way to learn the mechanics of iTraX, if you are successful in your application you will be working on a system similar to this (but on a much larger scale).

We have selected some apis and you may choose whichever one you like and write the code in the matching `core/biz_rule.py` file (please see the `Services` section below for details).

Your task can be broken down into three parts:

* Study the api docs of the _one_ service you have chosen.
* Write a biz_rule that consumes data from one of the api end points.
* Ingests that into our test system using the provided models.

To be clear; you will not need to write your own models, or edit existing models, nor are you expected to consume all the data the end point returns, some of these end points contain hundreds of megabytes of data, you can ingest as much data as you want to, but you do not have to consume everything.

### The Services

- https://pokemontcg.io/
- https://scryfall.com/docs/api
- https://developer.marvel.com/
- https://rapidapi.com/omgvamp/api/hearthstone


### Running your biz_rule

Running your integration (ingesting the data into the system) is as simple as `just bizrule`

### Solution

Problem-solving idea: 
1. understand table relationships (Service, Form, Object, Field) => using Foreign keys form a human readable table
Form (value) FK -> Object 
Object (Row) -> Service 
Field (Column name)  -> Service 
Service (table)
2. learn API behaviour (explore API endpoints using Insomnia, test different HTTP methods(GET, POST, etc.), understand parameters and headers(Authentication and API keys), determine endpoint/parameter to execute data queries)
3. learn API data structure (after I got successful response, understand json data structure, find the data of interests)
4. consume data: make the API request in Python
5. convert the raw data into format that the field expects of
5. ingest data: use the model provided to save the data to database
6. modulize the code to reduce the repetition in the code
7. customized error handing(manually) to guarantee the atomic transactions
8. found the Python decor to do the same thing as above

Pokemon visual data table:
SetName - TEXT
Series - TEXT
TotalCards - INTEGER
ReleaseDate - Date
symbol - URL

Marvel visual data table:
title - TEXT
pageCount - INTEGER
resourceURI - URL
price - FLOAT
