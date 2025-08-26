# navspec - Team Navigation Dashboard

A declarative dashboard tool that allows teams to version control and share their links.

## What is navspec?

navspec solves the problem of managing various tools and resources i.e. URLs across different environments (local, staging, testing, production) and functions (developers, operations, etc.). Instead of maintaining bookmarks or scattered documentation, navspec allows you to:

- Declaratively define URLs in YAML files
- Version control these definitions in Git repositories
- Share dashboards across teams and functions
- Customise locally with user preferences

## Use Cases

### Team Maintainers
1. Start a new repository for your team's dashboard
2. Install navspec as a tool
3. Create YAML configuration files
4. Run navspec locally to see live changes
5. Commit and push the YAML files
6. Share the repository with your team

### Team Members
1. Clone the shared repository
2. Install navspec tool
3. Run the tool to serve a localhost dashboard
4. Browse and access all links from one place

## Quick Start

### For Team Maintainers

1. **Create a new repository:**
```bash
mkdir my-dashboard
cd my-dashboard
git init
```

2. **Install navspec and create configuration:**
```bash
# Install navspec globally
pip install navspec

# Create default configuration
navspec init
```

3. **Edit the configuration:**
```yaml
# config/default.yaml
metadata:
  name: "Team Dashboard"
  description: "Our tools and resources"

categories:
  - name: "Development"
    links:
      - name: "Local Dev"
        url: "http://localhost:3000"
        description: "Local development server"
```

4. **Run and test:**
```bash
navspec serve
# Open http://localhost:7777
```

5. **Commit and share:**
```bash
git add .
git commit -m "Add team dashboard configuration"
git push
```

### For Team Members

1. **Clone the repository:**
```bash
git clone <team-dashboard-repo>
cd <team-dashboard-repo>
```

2. **Install and run:**
```bash
# Install navspec globally
pip install navspec

# Run from the repository (automatically finds config/ folder)
navspec serve
# Open http://localhost:7777
```


### Configuration Schema

```yaml
metadata:
  name: "Dashboard Name"
  description: "Description"
  version: "1.0.0"
  tags: ["tag1", "tag2"]

categories:
  - name: "Category Name"
    description: "Category description"
    icon: "icon-name"  # Optional
    links:
      - name: "Link Name"
        url: "https://example.com"
        description: "Link description"
        tags: ["tag1", "tag2"]
        status: "active"  # active, maintenance, down

user_preferences:
  default_config: "default.yaml"
  theme: "light"  # light, dark, auto
  layout: "grid"  # grid, list, compact
```

## Features

- **Live Reload**: See changes to YAML files immediately
- **Multiple Configurations**: Switch between different dashboards
- **Local Customisation**: User preferences stored locally
- **Tag-based Filtering**: Filter links by tags
- **Status Tracking**: Show service status (up/down/maintenance)
- **Responsive Design**: Works on desktop and mobile
- **Search**: Quick search through all links

## Installation

```bash
# Quick install from PyPI
pip install navspec

# Or install from source
git clone https://github.com/your-org/navspec
cd navspec
pip install -e .

# Or use the install script
./install.sh
```

## Development

```bash
git clone https://github.com/your-org/navspec
cd navspec

# Complete development setup
make dev-setup

# Or install manually:
pip install -r requirements.txt
pip install -e .
pre-commit install

# Common development commands:
make help              # Show all available commands
make format           # Format code with black and isort
make lint             # Run all linting tools
make test             # Run tests
make check-all        # Run format check, lint, and tests
make clean            # Clean up generated files

# Start development server
navspec serve

# Or run directly with Python
python -m navspec.cli serve
```

## Code Quality Tools

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting and style checking
- **mypy**: Type checking
- **bandit**: Security scanning
- **pre-commit**: Git hooks for automatic checks
- **pytest**: Testing framework

All tools are configured to work together seamlessly. Run `make format` to format your code before committing.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
