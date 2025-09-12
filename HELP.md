# Development Setup and Usage Guide

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

### Running your biz_rule

Running your code is as simple as `just bizrule`