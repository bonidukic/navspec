"""Command-line interface for navspec dashboard."""

import argparse
import sys
from pathlib import Path

from .server import create_server
from .config import ConfigManager


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="navspec - A declarative navigation dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  navspec serve                    # Serve dashboard from current directory
  navspec serve --port 7777       # Serve on port 7777
  navspec serve --config ./config # Serve from ./config directory
  navspec init                    # Initialize new dashboard configuration
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Serve the dashboard")
    serve_parser.add_argument(
        "--config", "-c",
        default=".",
        help="Path to configuration directory (default: current directory, will look for config/ subfolder)"
    )
    serve_parser.add_argument(
        "--port", "-p",
        type=int,
        default=7777,
        help="Port to serve on (default: 7777)"
    )
    serve_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    serve_parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload on file changes"
    )
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new dashboard configuration")
    init_parser.add_argument(
        "--config", "-c",
        default=".",
        help="Path to configuration directory (default: current directory, will create config/ subfolder)"
    )
    init_parser.add_argument(
        "--name",
        default="Company Dashboard",
        help="Dashboard name (default: 'Company Dashboard')"
    )
    init_parser.add_argument(
        "--description",
        default="Your company tools and resources",
        help="Dashboard description"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "serve":
        serve_dashboard(args)
    elif args.command == "init":
        init_dashboard(args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


def serve_dashboard(args):
    """Serve the dashboard."""
    config_path = Path(args.config).resolve()
    
    if not config_path.exists():
        print(f"Error: Configuration path does not exist: {config_path}")
        sys.exit(1)
    
    print(f"Starting navspec dashboard...")
    print(f"Configuration path: {config_path}")
    
    # Show where configs are actually loaded from
    config_manager = ConfigManager(str(config_path))
    actual_config_path = config_manager.config_path
    if actual_config_path != config_path:
        print(f"Loading configs from: {actual_config_path}")
        print(f"Tip: This project uses a 'config/' folder for organization")
    else:
        print(f"Loading configs from: {actual_config_path}")
        print(f"Tip: Create a 'config/' folder to organize multiple dashboards")
    
    print(f"Server: http://{args.host}:{args.port}")
    print(f"Press Ctrl+C to stop")
    print()
    
    try:
        server = create_server(
            config_path=str(config_path),
            port=args.port,
            host=args.host
        )
        server.run(reload=not args.no_reload)
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.stop()
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


def init_dashboard(args):
    """Initialize a new dashboard configuration."""
    config_path = Path(args.config).resolve()
    
    # Create config subdirectory for organized structure
    config_subdir = config_path / "config"
    if not config_subdir.exists():
        print(f"Creating configuration directory: {config_subdir}")
        config_subdir.mkdir(parents=True, exist_ok=True)
        print(f"This keeps your project root clean and organized")
    else:
        print(f"Using existing configuration directory: {config_subdir}")
    
    print(f"Initializing dashboard in: {config_subdir}")
    
    try:
        # Create config manager to generate default config
        config_manager = ConfigManager(str(config_path))
        
        # Check if configs already exist
        existing_configs = config_manager.get_available_configs()
        if existing_configs:
            print(f"WARNING: Found existing configurations: {', '.join(existing_configs)}")
            response = input("Do you want to overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Initialization cancelled.")
                return
        
        # Create default configuration
        config_manager._create_default_config()
        
        print("Dashboard initialized successfully!")
        print(f"Configuration files created in: {config_subdir}")
        print(f"Run 'navspec serve' to start the dashboard")
        print(f"Add more dashboards by creating new YAML files in the config/ folder")
        
    except Exception as e:
        print(f"ERROR: Error initializing dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
