// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Select all navigation links
    const navLinks = document.querySelectorAll('.nav-links a');

    // Add a click event listener to each link
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Only run custom smooth scrolling for internal links (starting with #)
            if (href.startsWith('#') && href.length > 1) {
                // Prevent the default jump behavior
                e.preventDefault(); 
                
                // Get the target element by its ID
                const targetElement = document.querySelector(href);

                if (targetElement) {
                    // Use the built-in browser smooth scroll function
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    // --- Carousel Logic for Reviews Section ---
    const reviewTrack = document.querySelector('.review-track');
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    const cards = document.querySelectorAll('.testimonial-card');

    if (reviewTrack && cards.length > 0) {
        const cardWidth = cards[0].offsetWidth + 20; // Card width + gap (20px)
        let currentIndex = 0;
        const totalCards = cards.length;
        // Assume only one card is visible at a time for simple scrolling
        const visibleCards = 1; 

        // Function to move the carousel
        const moveToCard = (index) => {
            // Calculate the horizontal offset
            reviewTrack.style.transform = `translateX(-${index * cardWidth}px)`;
            
            // Update currentIndex
            currentIndex = index;

            // Optional: Disable arrows at the start/end
            leftArrow.disabled = currentIndex === 0;
            rightArrow.disabled = currentIndex >= totalCards - visibleCards;
        };

        // Event listeners for arrows
        rightArrow.addEventListener('click', () => {
            if (currentIndex < totalCards - visibleCards) {
                moveToCard(currentIndex + 1);
            }
        });

        leftArrow.addEventListener('click', () => {
            if (currentIndex > 0) {
                moveToCard(currentIndex - 1);
            }
        });

        // Initialize carousel position
        moveToCard(0); // Start at the first card
    }
    // You can add more JavaScript here for scroll-based animations (like fading in content) 
    // as you add more sections.
});