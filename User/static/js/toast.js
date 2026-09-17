// toast.js
class ToastSystem {
    constructor() {
        this.container = document.getElementById('toast-container');
    }

    show(message, type = 'info') {
        if (!this.container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        let icon = 'fa-info-circle';
        if (type === 'success') icon = 'fa-check-circle';
        if (type === 'error') icon = 'fa-exclamation-circle';
        
        toast.innerHTML = `
            <div class="toast-icon">
                <i class="fa-solid ${icon}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">
                <i class="fa-solid fa-xmark"></i>
            </button>
        `;

        this.container.appendChild(toast);

        // GSAP Animation
        if (typeof gsap !== 'undefined') {
            gsap.fromTo(toast, 
                { x: 100, opacity: 0 },
                { x: 0, opacity: 1, duration: 0.4, ease: "back.out(1.7)" }
            );
        }

        // Close event
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => this.dismiss(toast));

        // Auto dismiss
        setTimeout(() => {
            this.dismiss(toast);
        }, 5000);
    }

    dismiss(toast) {
        if (typeof gsap !== 'undefined') {
            gsap.to(toast, {
                x: 100, 
                opacity: 0, 
                duration: 0.3, 
                ease: "power2.in",
                onComplete: () => toast.remove()
            });
        } else {
            toast.remove();
        }
    }
}

const Toasts = new ToastSystem();

// Parse Django messages on load
document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('django-messages');
    if (messagesContainer) {
        const messages = messagesContainer.querySelectorAll('.django-message');
        messages.forEach((msg, index) => {
            setTimeout(() => {
                const tags = msg.getAttribute('data-tags');
                const text = msg.innerText;
                let type = 'info';
                if (tags.includes('success')) type = 'success';
                if (tags.includes('error')) type = 'error';
                
                Toasts.show(text, type);
            }, index * 200); // Stagger toasts
        });
    }
});
