document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const previewPanes = document.querySelectorAll('.preview-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tab = this.dataset.tab;
            
            tabButtons.forEach(btn => btn.classList.remove('active'));
            previewPanes.forEach(pane => pane.classList.remove('active'));
            
            this.classList.add('active');
            const targetPane = document.getElementById(`preview-${tab}`);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });
    
    const images = document.querySelectorAll('img[data-src]');
    if (images.length > 0) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
});
