// app.js

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Password Visibility Toggle
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const input = toggle.parentElement.querySelector('input');
            const icon = toggle.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // 2. Mobile Sidebar Toggle
    const menuBtn = document.getElementById('mobile-menu-btn');
    const closeSidebarBtn = document.getElementById('close-sidebar-btn');
    const sidebar = document.getElementById('sidebar');

    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', () => {
            sidebar.classList.add('open');
        });
    }

    if (closeSidebarBtn && sidebar) {
        closeSidebarBtn.addEventListener('click', () => {
            sidebar.classList.remove('open');
        });
    }

    // 3. Page Entrance Animations (GSAP)
    if (typeof gsap !== 'undefined') {
        
        // Auth Layout Animation
        if (document.querySelector('.auth-card')) {
            gsap.fromTo('.auth-card',
                { y: 30, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }
            );
            
            if (document.querySelector('.auth-visual')) {
                gsap.fromTo('.auth-brand',
                    { x: -30, opacity: 0 },
                    { x: 0, opacity: 1, duration: 0.8, delay: 0.2, ease: "power3.out" }
                );
                gsap.fromTo('.auth-quote',
                    { y: 30, opacity: 0 },
                    { y: 0, opacity: 1, duration: 0.8, delay: 0.4, ease: "power3.out" }
                );
            }
        }
        
        // Dashboard Animations
        if (document.querySelector('.main-content')) {
            gsap.fromTo('.page-header',
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.6, ease: "power2.out" }
            );
            
            gsap.fromTo('.stat-card',
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power2.out", delay: 0.2 }
            );
            
            gsap.fromTo('.contact-card, .data-row',
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, stagger: 0.05, ease: "power2.out", delay: 0.3 }
            );
        }
    }
});
