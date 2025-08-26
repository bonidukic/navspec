"""Type definitions for navspec dashboard configuration."""

from typing import Any, Dict, List, Literal, Optional


class DashboardMetadata:
    """Metadata for a dashboard configuration."""

    def __init__(self, name: str, description: str, version: str, tags: List[str]):
        self.name = name
        self.description = description
        self.version = version
        self.tags = tags

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DashboardMetadata":
        return cls(
            name=data["name"],
            description=data["description"],
            version=data["version"],
            tags=data["tags"],
        )


class Link:
    """A single link in a category."""

    def __init__(
        self,
        name: str,
        url: str,
        description: str,
        tags: List[str],
        status: str = "active",
        icon: Optional[str] = None,
    ):
        self.name = name
        self.url = url
        self.description = description
        self.tags = tags
        self.status = status
        self.icon = icon

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "tags": self.tags,
            "status": self.status,
            "icon": self.icon,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Link":
        return cls(
            name=data["name"],
            url=data["url"],
            description=data["description"],
            tags=data["tags"],
            status=data.get("status", "active"),
            icon=data.get("icon"),
        )


class Category:
    """A category containing multiple links."""

    def __init__(
        self, name: str, description: str, links: List[Link], icon: Optional[str] = None
    ):
        self.name = name
        self.description = description
        self.icon = icon
        self.links = links

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "links": [link.to_dict() for link in self.links],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        return cls(
            name=data["name"],
            description=data["description"],
            icon=data.get("icon"),
            links=[Link.from_dict(link_data) for link_data in data["links"]],
        )


class DashboardConfig:
    """Complete dashboard configuration."""

    def __init__(self, metadata: DashboardMetadata, categories: List[Category]):
        self.metadata = metadata
        self.categories = categories

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "categories": [category.to_dict() for category in self.categories],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DashboardConfig":
        return cls(
            metadata=DashboardMetadata.from_dict(data["metadata"]),
            categories=[
                Category.from_dict(cat_data) for cat_data in data["categories"]
            ],
        )


class UserPreferences:
    """User-specific preferences stored locally."""

    def __init__(
        self,
        active_config: str = "default.yaml",
        theme: str = "light",
        layout: str = "grid",
        show_descriptions: bool = True,
        show_status: bool = True,
        custom_order: List[str] = None,
        recent_links: List[str] = None,
    ):
        self.active_config = active_config
        self.theme = theme
        self.layout = layout
        self.show_descriptions = show_descriptions
        self.show_status = show_status
        self.custom_order = custom_order or []
        self.recent_links = recent_links or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "active_config": self.active_config,
            "theme": self.theme,
            "layout": self.layout,
            "show_descriptions": self.show_descriptions,
            "show_status": self.show_status,
            "custom_order": self.custom_order,
            "recent_links": self.recent_links,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserPreferences":
        return cls(
            active_config=data.get("active_config", "default.yaml"),
            theme=data.get("theme", "light"),
            layout=data.get("layout", "grid"),
            show_descriptions=data.get("show_descriptions", True),
            show_status=data.get("show_status", True),
            custom_order=data.get("custom_order", []),
            recent_links=data.get("recent_links", []),
        )


class UserConfig:
    """User configuration combining preferences and available configs."""

    def __init__(
        self,
        config_path: str,
        preferences: UserPreferences,
        available_configs: List[str],
    ):
        self.config_path = config_path
        self.preferences = preferences
        self.available_configs = available_configs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config_path": self.config_path,
            "preferences": self.preferences.to_dict(),
            "available_configs": self.available_configs,
        }


class ServerOptions:
    """Server configuration options."""

    def __init__(
        self,
        port: int = 7777,
        host: str = "127.0.0.1",
        config_path: str = ".",
        watch: bool = True,
        reload: bool = True,
    ):
        self.port = port
        self.host = host
        self.config_path = config_path
        self.watch = watch
        self.reload = reload
