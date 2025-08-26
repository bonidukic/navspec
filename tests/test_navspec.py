#!/usr/bin/env python3
"""
Simple test script for navspec
Run this to verify the installation works correctly
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from navspec.types import Category, DashboardConfig, DashboardMetadata, Link

        print("Types imported successfully")
    except ImportError as e:
        print(f"ERROR: Failed to import types: {e}")
        return False

    try:
        from navspec.config import ConfigManager

        print("ConfigManager imported successfully")
    except ImportError as e:
        print(f"ERROR: Failed to import ConfigManager: {e}")
        return False

    try:
        from navspec.server import create_server

        print("Server imported successfully")
    except ImportError as e:
        print(f"ERROR: Failed to import server: {e}")
        return False

    return True


def test_config_creation():
    """Test configuration creation."""
    print("\nTesting configuration creation...")

    try:
        from navspec.config import ConfigManager

        # Create a temporary config directory
        test_dir = Path("test_config")
        test_dir.mkdir(exist_ok=True)

        # Initialize config manager
        config_manager = ConfigManager(str(test_dir))

        # Check if default config was created
        configs = config_manager.get_available_configs()
        if "default.yaml" in configs:
            print("Default configuration created successfully")
        else:
            print("ERROR: Default configuration not found")
            return False

        # Load the config
        config = config_manager.load_config()
        if config:
            print("Configuration loaded successfully")
            print(f"   Dashboard: {config.metadata.name}")
            print(f"   Categories: {len(config.categories)}")
        else:
            print("ERROR: Failed to load configuration")
            return False

        # Cleanup
        import shutil

        shutil.rmtree(test_dir)

        return True

    except Exception as e:
        print(f"ERROR: Configuration test failed: {e}")
        return False


def test_yaml_parsing():
    """Test YAML parsing with example configs."""
    print("\nTesting YAML parsing...")

    try:
        import yaml

        from navspec.types import DashboardConfig

        # Test with our example config
        example_file = Path("config/default.yaml")
        if not example_file.exists():
            print("ERROR: Example configuration file not found")
            return False

        with open(example_file, "r") as f:
            data = yaml.safe_load(f)

        # Validate with our types
        config = DashboardConfig.from_dict(data)
        print("Example configuration parsed successfully")
        print(f"   Dashboard: {config.metadata.name}")
        print(f"   Categories: {len(config.categories)}")

        # Check some specific data
        dev_category = next(
            (cat for cat in config.categories if cat.name == "Development"), None
        )
        if dev_category:
            print(f"   Development links: {len(dev_category.links)}")

        return True

    except Exception as e:
        print(f"ERROR: YAML parsing test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 navspec Test Suite")
    print("==================")

    tests = [
        test_imports,
        test_config_creation,
        test_yaml_parsing,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! navspec is ready to use.")
        print("\nNext steps:")
        print("1. Run: navspec init")
        print("2. Run: navspec serve")
        print("3. Open http://localhost:7777 in your browser")
    else:
        print("ERROR: Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
