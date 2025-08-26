"""Flask server for navspec dashboard."""

from pathlib import Path
from typing import Optional
from flask import Flask, request, jsonify, send_from_directory
import os

from .config import ConfigManager
from .types import DashboardConfig, UserPreferences


class DashboardServer:
    """Flask server for serving the dashboard."""
    
    def __init__(self, config_path: str = ".", port: int = 7777, host: str = "127.0.0.1"):
        self.config_manager = ConfigManager(config_path)
        self.port = port
        self.host = host
        
        # Create Flask app
        self.app = Flask(__name__)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes and static file serving."""
        
        # API endpoints
        @self.app.route("/api/config")
        def get_config():
            """Get dashboard configuration."""
            config_name = request.args.get('config_name')
            config = self.config_manager.load_config(config_name)
            if config is None:
                return jsonify({"error": "Configuration not found"}), 404
            return jsonify(config.to_dict())
        
        @self.app.route("/api/user-config")
        def get_user_config():
            """Get user configuration and preferences."""
            return jsonify(self.config_manager.get_user_config().to_dict())
        
        @self.app.route("/api/preferences", methods=['POST'])
        def update_preferences():
            """Update user preferences."""
            try:
                data = request.get_json()
                self.config_manager.update_user_preferences(**data)
                return jsonify({"status": "success"})
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        @self.app.route("/api/configs")
        def get_available_configs():
            """Get list of available configuration files."""
            return jsonify({
                "configs": self.config_manager.get_available_configs(),
                "active": self.config_manager.user_preferences.active_config
            })
        
        # Main dashboard page
        @self.app.route("/")
        def dashboard():
            """Serve the main dashboard page."""
            return self._render_dashboard()
        
        # Health check
        @self.app.route("/health")
        def health_check():
            """Health check endpoint."""
            return jsonify({"status": "healthy"})
        
        # Static files
        @self.app.route("/static/<path:filename>")
        def static_files(filename):
            """Serve static files."""
            static_dir = os.path.join(os.path.dirname(__file__), 'static')
            return send_from_directory(static_dir, filename)
    
    def _render_dashboard(self) -> str:
        """Render the dashboard HTML."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>navspec Dashboard</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div id="app">
        <header class="dashboard-header">
            <h1>navspec Dashboard</h1>
            <div class="config-selector">
                <select id="configSelect">
                    <option value="">Loading...</option>
                </select>
            </div>
        </header>
        
        <main class="dashboard-content">
            <div id="dashboard" class="dashboard-grid">
                <div class="loading">Loading dashboard...</div>
            </div>
        </main>
        
        <div class="preferences-panel">
            <button id="preferencesBtn">Preferences</button>
        </div>
    </div>
    
    <script src="/static/app.js"></script>
</body>
</html>
        """
    
    def run(self, reload: bool = True):
        """Run the server."""
        debug_mode = reload
        self.app.run(
            host=self.host,
            port=self.port,
            debug=debug_mode
        )
    
    def stop(self):
        """Stop the server and cleanup."""
        self.config_manager.stop_file_watching()


def create_server(config_path: str = ".", port: int = 7777, host: str = "127.0.0.1") -> DashboardServer:
    """Create and return a dashboard server instance."""
    return DashboardServer(config_path, port, host)
