function renderHeader(rootPath) {
    // Determine current page for active state
    const currentPath = window.location.pathname;
    const isWork = currentPath.includes('work.html');
    const isAbout = currentPath.includes('about.html');
    const isBlog = currentPath.includes('blog') || currentPath.includes('pyspark') || currentPath.includes('search') || currentPath.includes('crawler');
    const isContact = currentPath.includes('contact.html');

    // Helper to get correct path
    const getPath = (path) => {
        if (rootPath === '.') return path;
        return `${rootPath}/${path}`;
    };

    const headerHTML = `
    <header>
        <div class="container">
            <nav>
                <div class="logo">
                     <a href="${getPath('index.html')}" style="color: inherit;"><span style="color: var(--accent-color)">></span> _mediumroast</a>
                </div>
                <button class="mobile-menu-btn" aria-label="Toggle Menu">
                    ☰
                </button>
                <div class="nav-links">
                    <a href="${getPath('work.html')}" class="${isWork ? 'active' : ''}">Work</a>
                    <a href="${getPath('about.html')}" class="${isAbout ? 'active' : ''}">About</a>
                    <a href="${getPath('blog.html')}" class="${isBlog ? 'active' : ''}">Blog</a>
                    <a href="${getPath('contact.html')}" class="${isContact ? 'active' : ''}">Contact</a>
                    <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" title="Toggle light/dark mode">
                        <svg class="theme-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <!-- Coffee bean icon (dark mode) -->
                            <path class="coffee-bean" d="M12 2C8.5 2 6 4.5 6 8c0 2.5 1.5 4.5 3.5 5.5C8 14.5 7 16 7 18c0 3.5 2.5 6 5 6s5-2.5 5-6c0-2-1-3.5-2.5-4.5C16.5 12.5 18 10.5 18 8c0-3.5-2.5-6-6-6zm0 2c2.5 0 4 2 4 4 0 1.5-1 3-2.5 3.5-.5-.5-1-1-1.5-1.5-.5.5-1 1-1.5 1.5C9 11 8 9.5 8 8c0-2 1.5-4 4-4zm0 16c-2 0-3-1.5-3-4 0-1.5.5-2.5 1.5-3.5.5.5 1 1 1.5 1.5.5-.5 1-1 1.5-1.5 1 1 1.5 2 1.5 3.5 0 2.5-1 4-3 4z"/>
                            <!-- Coffee flower icon (light mode) -->
                            <path class="coffee-flower" d="M12 2c-1.1 0-2 .9-2 2 0 .7.4 1.3 1 1.7-.6.4-1 1-1 1.8 0 1.1.9 2 2 2s2-.9 2-2c0-.8-.4-1.4-1-1.8.6-.4 1-1 1-1.7 0-1.1-.9-2-2-2zm-5 6c-1.1 0-2 .9-2 2 0 .7.4 1.3 1 1.7-.6.4-1 1-1 1.8 0 1.1.9 2 2 2s2-.9 2-2c0-.8-.4-1.4-1-1.8.6-.4 1-1 1-1.7 0-1.1-.9-2-2-2zm10 0c-1.1 0-2 .9-2 2 0 .7.4 1.3 1 1.7-.6.4-1 1-1 1.8 0 1.1.9 2 2 2s2-.9 2-2c0-.8-.4-1.4-1-1.8.6-.4 1-1 1-1.7 0-1.1-.9-2-2-2zm-5 6c-1.1 0-2 .9-2 2 0 .7.4 1.3 1 1.7-.6.4-1 1-1 1.8 0 1.1.9 2 2 2s2-.9 2-2c0-.8-.4-1.4-1-1.8.6-.4 1-1 1-1.7 0-1.1-.9-2-2-2z"/>
                        </svg>
                    </button>
                </div>
            </nav>
        </div>
    </header>
    `;

    document.getElementById('site-header').innerHTML = headerHTML;

    // Initialize theme
    initializeTheme();

    // Mobile Menu Logic
    setTimeout(() => {
        const btn = document.querySelector('.mobile-menu-btn');
        const nav = document.querySelector('.nav-links');
        if (btn && nav) {
            btn.onclick = () => nav.classList.toggle('active');
        }

        // Theme toggle logic
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.onclick = toggleTheme;
        }
    }, 0);
}

// Theme management functions
function initializeTheme() {
    // Check for saved theme preference or default to system preference
    const savedTheme = localStorage.getItem('theme');
    let theme;
    
    if (savedTheme) {
        theme = savedTheme;
    } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = prefersDark ? 'dark' : 'dark'; // Default to dark if no system preference
    }
    
    document.documentElement.setAttribute('data-theme', theme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
