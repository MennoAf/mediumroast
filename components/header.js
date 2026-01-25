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
                     <a href="${getPath('index.html')}" style="color: inherit;"><span style="color: var(--accent-color)">></span> jason_bauman</a>
                </div>
                <button class="mobile-menu-btn" aria-label="Toggle Menu">
                    ☰
                </button>
                <div class="nav-links">
                    <a href="${getPath('work.html')}" class="${isWork ? 'active' : ''}">Work</a>
                    <a href="${getPath('about.html')}" class="${isAbout ? 'active' : ''}">About</a>
                    <a href="${getPath('blog.html')}" class="${isBlog ? 'active' : ''}">Blog</a>
                    <a href="${getPath('contact.html')}" class="${isContact ? 'active' : ''}">Contact</a>
                </div>
            </nav>
        </div>
    </header>
    `;

    document.getElementById('site-header').innerHTML = headerHTML;

    // Mobile Menu Logic
    setTimeout(() => {
        const btn = document.querySelector('.mobile-menu-btn');
        const nav = document.querySelector('.nav-links');
        if (btn && nav) {
            btn.onclick = () => nav.classList.toggle('active');
        }
    }, 0);
}
