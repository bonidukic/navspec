// navspec Dashboard JavaScript

class DashboardApp {
    constructor() {
        this.currentConfig = null;
        this.userPreferences = null;
        this.availableConfigs = [];
        
        this.init();
    }
    
    async init() {
        try {
            // Load user configuration
            await this.loadUserConfig();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Load initial dashboard
            await this.loadDashboard();
            
        } catch (error) {
            console.error('Failed to initialize dashboard:', error);
            this.showError('Failed to initialize dashboard');
        }
    }
    
    async loadUserConfig() {
        try {
            const response = await fetch('/api/user-config');
            const userConfig = await response.json();
            
            this.userPreferences = userConfig.preferences;
            this.availableConfigs = userConfig.available_configs;
            
            // Populate config selector
            this.populateConfigSelector();
            
        } catch (error) {
            console.error('Failed to load user config:', error);
        }
    }
    
    populateConfigSelector() {
        const selector = document.getElementById('configSelect');
        if (!selector) return;
        
        selector.innerHTML = '';
        
        this.availableConfigs.forEach(configName => {
            const option = document.createElement('option');
            option.value = configName;
            option.textContent = configName.replace('.yaml', '');
            
            if (configName === this.userPreferences.active_config) {
                option.selected = true;
            }
            
            selector.appendChild(option);
        });
    }
    
    async loadDashboard(configName = null) {
        try {
            const url = configName ? `/api/config?config_name=${configName}` : '/api/config';
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            this.currentConfig = await response.json();
            this.renderDashboard();
            
        } catch (error) {
            console.error('Failed to load dashboard:', error);
            this.showError('Failed to load dashboard configuration');
        }
    }
    
    renderDashboard() {
        const dashboardElement = document.getElementById('dashboard');
        if (!dashboardElement || !this.currentConfig) return;
        
        const { metadata, categories } = this.currentConfig;
        
        // Update page title
        document.title = `${metadata.name} - navspec Dashboard`;
        
        // Update header
        const headerTitle = document.querySelector('.dashboard-header h1');
        if (headerTitle) {
            headerTitle.textContent = metadata.name;
        }
        
        // Render categories
        dashboardElement.innerHTML = this.renderCategories(categories);
        
        // Add click handlers to links
        this.setupLinkHandlers();
    }
    
    renderCategories(categories) {
        if (!categories || categories.length === 0) {
            return '<div class="loading">No categories found</div>';
        }
        
        return categories.map(category => this.renderCategory(category)).join('');
    }
    
    renderCategory(category) {
        const { name, description, icon, links } = category;
        
        return `
            <div class="category-card">
                <div class="category-header">
                    <h3>${this.escapeHtml(name)}</h3>
                    <div class="category-description">${this.escapeHtml(description)}</div>
                    ${icon ? `<div class="category-icon">${icon}</div>` : ''}
                </div>
                <div class="links-grid">
                    ${this.renderLinks(links)}
                </div>
            </div>
        `;
    }
    
    renderLinks(links) {
        if (!links || links.length === 0) {
            return '<div class="no-links">No links in this category</div>';
        }
        
        return links.map(link => this.renderLink(link)).join('');
    }
    
    renderLink(link) {
        const { name, url, description, tags, status, icon } = link;
        
        const statusClass = status || 'active';
        const statusText = status || 'active';
        
        return `
            <a href="${this.escapeHtml(url)}" class="link-card" target="_blank" rel="noopener noreferrer">
                <div class="link-info">
                    <div class="link-name">${this.escapeHtml(name)}</div>
                    <div class="link-description">${this.escapeHtml(description)}</div>
                    <div class="link-url">${this.escapeHtml(url)}</div>
                    ${this.renderTags(tags)}
                </div>
                <div class="link-status ${statusClass}">${statusText}</div>
            </a>
        `;
    }
    
    renderTags(tags) {
        if (!tags || tags.length === 0) return '';
        
        return `
            <div class="link-tags">
                ${tags.map(tag => `<span class="tag">${this.escapeHtml(tag)}</span>`).join('')}
            </div>
        `;
    }
    
    setupLinkHandlers() {
        const links = document.querySelectorAll('.link-card');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                this.handleLinkClick(e, link);
            });
        });
    }
    
    handleLinkClick(event, linkElement) {
        const url = linkElement.href;
        const linkName = linkElement.querySelector('.link-name').textContent;
        
        // Track recent links
        this.addRecentLink(linkName);
        
        // Open link in new tab (already handled by target="_blank")
        console.log(`Opening link: ${linkName} -> ${url}`);
    }
    
    addRecentLink(linkName) {
        if (!this.userPreferences.recent_links) {
            this.userPreferences.recent_links = [];
        }
        
        // Remove if already exists
        this.userPreferences.recent_links = this.userPreferences.recent_links.filter(
            name => name !== linkName
        );
        
        // Add to beginning
        this.userPreferences.recent_links.unshift(linkName);
        
        // Keep only last 10
        this.userPreferences.recent_links = this.userPreferences.recent_links.slice(0, 10);
        
        // Save preferences
        this.saveUserPreferences();
    }
    
    async saveUserPreferences() {
        try {
            const response = await fetch('/api/preferences', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.userPreferences),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
        } catch (error) {
            console.error('Failed to save preferences:', error);
        }
    }
    
    setupEventListeners() {
        // Config selector change
        const configSelector = document.getElementById('configSelect');
        if (configSelector) {
            configSelector.addEventListener('change', (e) => {
                this.handleConfigChange(e.target.value);
            });
        }
        
        // Preferences button
        const preferencesBtn = document.getElementById('preferencesBtn');
        if (preferencesBtn) {
            preferencesBtn.addEventListener('click', () => {
                this.showPreferences();
            });
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    }
    
    async handleConfigChange(configName) {
        try {
            this.userPreferences.active_config = configName;
            await this.saveUserPreferences();
            await this.loadDashboard(configName);
        } catch (error) {
            console.error('Failed to change config:', error);
        }
    }
    
    showPreferences() {
        // Simple preferences modal for now
        // In v2, this could be a full preferences panel
        alert('Preferences panel coming in v2!');
    }
    
    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + K for search (future feature)
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            // TODO: Implement search
            console.log('Search shortcut pressed');
        }
        
        // Ctrl/Cmd + R to refresh
        if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
            event.preventDefault();
            this.loadDashboard();
        }
    }
    
    showError(message) {
        const dashboardElement = document.getElementById('dashboard');
        if (dashboardElement) {
            dashboardElement.innerHTML = `
                <div class="error-message">
                    <h3>Error</h3>
                    <p>${this.escapeHtml(message)}</p>
                    <button onclick="location.reload()">Retry</button>
                </div>
            `;
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DashboardApp();
});

// Add some utility functions to global scope for debugging
window.DashboardApp = DashboardApp;
