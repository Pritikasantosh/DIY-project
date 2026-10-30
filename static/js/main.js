/**
 * Flask Blogging Platform - Week 4 JavaScript Enhancements
 * Features: Mobile menu toggle, auto-dismissing alerts, and reading progress bar
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // 1. Mobile Hamburger Menu Toggle
    // -------------------------------------------------------------
    const menuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');

    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', () => {
            menuBtn.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Close mobile menu if clicked outside
        document.addEventListener('click', (e) => {
            if (!menuBtn.contains(e.target) && !navLinks.contains(e.target)) {
                menuBtn.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }

    // -------------------------------------------------------------
    // 2. Flash Messages Dismissal
    // -------------------------------------------------------------
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        // Manual close button
        const closeBtn = alert.querySelector('.alert-close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissAlert(alert);
            });
        }

        // Auto-dismiss after 4.5 seconds
        setTimeout(() => {
            dismissAlert(alert);
        }, 4500);
    });

    function dismissAlert(alertElement) {
        alertElement.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        alertElement.style.opacity = '0';
        alertElement.style.transform = 'translateY(-8px)';
        setTimeout(() => {
            if (alertElement.parentElement) {
                alertElement.remove();
            }
        }, 400);
    }

    // -------------------------------------------------------------
    // 3. Reading Progress Bar (for Single Post Page)
    // -------------------------------------------------------------
    const progressBar = document.getElementById('readingProgressBar');
    const postBody = document.querySelector('.single-post-body');

    if (progressBar && postBody) {
        window.addEventListener('scroll', () => {
            const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
            if (totalHeight > 0) {
                const scrolled = (window.scrollY / totalHeight) * 100;
                progressBar.style.width = `${Math.min(100, Math.max(0, scrolled))}%`;
            }
        });
    }
});
