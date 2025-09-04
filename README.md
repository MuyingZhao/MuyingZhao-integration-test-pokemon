# README

## Purpose

This is a scale model of torx make, with the basic models and a simple api, it uses django rest framework to create a viewable api in the browser.

It is designed as a way to learn the mechanics of torx make.

## Development Environment Setup

### Installing Devbox

This project uses [devbox](https://www.jetify.com/devbox) to manage the development environment. Devbox provides an isolated, reproducible development environment with all necessary tools.

#### Windows (WSL recommended)

1. **Install WSL2** (if not already installed):
   ```powershell
   wsl --install
   ```
   Restart your computer and set up a Linux distribution (Ubuntu recommended).

2. **Inside WSL2**, install devbox:
   ```bash
   curl -fsSL https://get.jetify.com/devbox | bash
   ```

#### macOS

Install using Homebrew:
```bash
brew install jetify-io/devbox/devbox
```

Or using the install script:
```bash
curl -fsSL https://get.jetify.com/devbox | bash
```

#### Linux

```bash
curl -fsSL https://get.jetify.com/devbox | bash
```

### Setting up the Project

1. **Clone and enter the project directory**:
   ```bash
   git clone <repository-url>
   cd integrations-test
   ```

2. **Start the devbox shell**:
   ```bash
   devbox shell
   ```
   This will automatically install `just` and Docker tools. Python and linting tools are available in the Docker container.

3. **Run the setup script** (optional):
   ```bash
   devbox run setup
   ```

4. **Set up environment variables**:
   Copy `env.example` to `.env` and configure as needed:
   ```bash
   cp env.example .env
   ```

## Project Commands

This project uses [just](https://github.com/casey/just) as a command runner (replacing the previous Makefile). All commands should be run within the devbox shell.

### Basic Setup Commands

To build the docker image: `just build`

To generate migrations: `just migrations`

To apply migrations: `just migrate`

To create a super user: `just createsuperuser`

To run the web server: `just start`

To read the logs: `just logs`

### Available Commands

Run `just help` or `just` to see all available commands with detailed descriptions.

## Usage

There is a web server that starts up and runs on: http://localhost:8000/

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
