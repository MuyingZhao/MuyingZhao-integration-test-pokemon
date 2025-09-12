# README

## Purpose

This is a scale model of torx make, with the basic models and a simple api, it uses django rest framework to create a viewable api in the browser.

It is designed as a way to learn the mechanics of torx make.

## Setup

For development environment setup, project commands, and usage instructions, please see [HELP.md](HELP.md).

## The test

### Description Of Problem

At Elixir we often have to work with third party apis and ingest data into our system, we write bespoke programs that we call `biz_rules` to perform this integration. This test is a scale model of the sort of work we do quite frequently and is quite reflective of what a typical day might look like.

We have selected some apis and you may choose whichever one you like and write the code in the matching `core/biz_rule.py` file (please see the `Services` section below for details).

Your task can be broken down into three parts:

* Study the api docs of the service you have chosen.
* Write a biz_rule that consumes data from one of the api end points.
* Ingests that into our test system using the provided models.

Please note: You will not need to write your own models!

### The Services

- https://pokemontcg.io/
- https://scryfall.com/docs/api
- https://developer.marvel.com/
- https://rapidapi.com/omgvamp/api/hearthstone


### Running your biz_rule

Running your code is as simple as `just bizrule`

For detailed setup and usage instructions, see [HELP.md](HELP.md).
