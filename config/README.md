# navspec Configuration Files

This folder contains your dashboard configuration files. Each YAML file represents a different dashboard view.

## File Structure

```
config/
├── default.yaml          # Main dashboard (loaded by default)
├── developers.yaml       # Developer-specific tools
├── operations.yaml       # Operations and monitoring tools
└── qa.yaml              # Quality assurance tools
```

## How It Works

1. **Default Loading**: navspec automatically looks for `config/` folder in your project
2. **Multiple Dashboards**: Create different YAML files for different teams/functions
3. **Easy Switching**: Users can switch between dashboards using the dropdown
4. **Version Control**: All configs are version controlled and shared with your team

## Creating New Dashboards

1. **Copy an existing config**: `cp default.yaml my-team.yaml`
2. **Edit the metadata**: Change name, description, and tags
3. **Customise categories**: Add/remove categories and links for your team
4. **Test locally**: Run `navspec serve` to see your changes

## Example Structure

```yaml
metadata:
  name: "My Team Dashboard"
  description: "Tools and resources for my team"
  version: "1.0.0"
  tags: ["my-team", "custom"]

categories:
  - name: "Team Tools"
    description: "Tools specific to our team"
    links:
      - name: "Team Wiki"
        url: "https://wiki.company.com/my-team"
        description: "Our team documentation"
        tags: ["docs", "team"]
        status: "active"
```

## Best Practices

- **Use descriptive names**: `developers.yaml`, `operations.yaml`, not `team1.yaml`
- **Add meaningful tags**: Help users find and filter tools
- **Keep descriptions clear**: Explain what each tool is for
- **Update status**: Mark tools as `active`, `maintenance`, or `down`
- **Version your configs**: Update version numbers when making changes

## Sharing with Your Team

1. **Commit your configs**: `git add config/ && git commit -m "Add team dashboard"`
2. **Push to shared repo**: `git push origin main`
3. **Team members clone**: They get all dashboards automatically
4. **Local customisation**: Each user can set their preferred default dashboard
