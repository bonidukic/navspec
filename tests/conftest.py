"""
Test configuration and shared fixtures for navspec tests.
"""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for test configurations."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_config():
    """Sample configuration data for testing."""
    return {
        "metadata": {
            "name": "Test Dashboard",
            "description": "Test dashboard for unit tests",
            "version": "1.0.0"
        },
        "categories": [
            {
                "name": "Test Category",
                "description": "Test category description",
                "links": [
                    {
                        "name": "Test Link",
                        "url": "https://example.com",
                        "description": "Test link description"
                    }
                ]
            }
        ]
    }

