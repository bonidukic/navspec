"""Configuration management for navspec dashboard."""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .types import DashboardConfig, UserPreferences, UserConfig, DashboardMetadata, Category, Link


class ConfigManager:
    """Manages dashboard configuration files and user preferences."""
    
    def __init__(self, config_path: str = "."):
        self.config_path = Path(config_path).resolve()
        
        # Look for configs in config/ subdirectory by default
        # This is for development and organized projects
        if (self.config_path / "config").exists():
            self.config_path = self.config_path / "config"
        
        # User config directory is always in the project root (not in config/ subfolder)
        self.user_config_dir = Path(config_path).resolve() / ".navspec"
        self.user_config_file = self.user_config_dir / "preferences.json"
        
        # Ensure user config directory exists
        self.user_config_dir.mkdir(exist_ok=True)
        
        # Load or create user preferences
        self.user_preferences = self._load_user_preferences()
        
        # File watching
        self.observer = None
        self._start_file_watching()
    
    def _load_user_preferences(self) -> UserPreferences:
        """Load user preferences from local file."""
        if self.user_config_file.exists():
            try:
                with open(self.user_config_file, 'r') as f:
                    data = json.load(f)
                    return UserPreferences.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Return default preferences
        return UserPreferences()
    
    def _save_user_preferences(self):
        """Save user preferences to local file."""
        with open(self.user_config_file, 'w') as f:
            json.dump(self.user_preferences.to_dict(), f, indent=2)
    
    def get_available_configs(self) -> List[str]:
        """Get list of available YAML configuration files."""
        configs = []
        for file_path in self.config_path.glob("*.yaml"):
            if file_path.name != ".navspec":  # Skip hidden directories
                configs.append(file_path.name)
        
        # Ensure default.yaml exists, create if not
        if not configs or "default.yaml" not in configs:
            self._create_default_config()
            configs = ["default.yaml"]
        
        return sorted(configs)
    
    def _create_default_config(self):
        """Create a default configuration file if none exists."""
        default_config = DashboardConfig(
            metadata=DashboardMetadata(
                name="Company Dashboard",
                description="Your company tools and resources",
                version="1.0.0",
                tags=["default"]
            ),
            categories=[
                Category(
                    name="Development",
                    description="Development tools and environments",
                    links=[
                        Link(
                            name="Local Development",
                            url="http://localhost:3000",
                            description="Local development server",
                            tags=["dev", "local"],
                            status="active"
                        )
                    ]
                )
            ]
        )
        
        with open(self.config_path / "default.yaml", 'w') as f:
            yaml.dump(default_config.to_dict(), f, default_flow_style=False, indent=2)
    
    def load_config(self, config_name: str = None) -> Optional[DashboardConfig]:
        """Load a specific configuration file."""
        if config_name is None:
            config_name = self.user_preferences.active_config
        
        config_file = self.config_path / config_name
        if not config_file.exists():
            return None
        
        try:
            with open(config_file, 'r') as f:
                data = yaml.safe_load(f)
                return DashboardConfig.from_dict(data)
        except (yaml.YAMLError, KeyError) as e:
            print(f"Error loading config {config_name}: {e}")
            return None
    
    def save_config(self, config: DashboardConfig, config_name: str):
        """Save a configuration to a YAML file."""
        config_file = self.config_path / config_name
        with open(config_file, 'w') as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, indent=2)
    
    def update_user_preferences(self, **kwargs):
        """Update user preferences."""
        for key, value in kwargs.items():
            if hasattr(self.user_preferences, key):
                setattr(self.user_preferences, key, value)
        
        self._save_user_preferences()
    
    def get_user_config(self) -> UserConfig:
        """Get complete user configuration."""
        return UserConfig(
            config_path=str(self.config_path),
            preferences=self.user_preferences,
            available_configs=self.get_available_configs()
        )
    
    def _start_file_watching(self):
        """Start watching for configuration file changes."""
        if self.observer is None:
            self.observer = Observer()
            event_handler = ConfigFileHandler(self)
            self.observer.schedule(event_handler, str(self.config_path), recursive=False)
            self.observer.start()
    
    def stop_file_watching(self):
        """Stop watching for file changes."""
        if self.observer:
            self.observer.stop()
            self.observer.join()


class ConfigFileHandler(FileSystemEventHandler):
    """Handles file system events for configuration files."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith('.yaml'):
            print(f"Configuration file changed: {event.src_path}")
            # In future versions, we might want to notify the server
            # to reload the configuration or refresh the UI
