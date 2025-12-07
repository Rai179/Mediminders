
        let currentIndex = 0;

        function slideReviews(direction) {
            const track = document.getElementById('reviewTrack');
            const cards = track.getElementsByClassName('testimonial-card');
            const totalCards = cards.length;

            if (totalCards === 0) return;

            currentIndex += direction;

            if (currentIndex < 0) {
                currentIndex = totalCards - 1;
            } else if (currentIndex >= totalCards) {
                currentIndex = 0;
            }

            const cardWidth = cards[0].offsetWidth;
            const gap = 30;
            const offset = -(currentIndex * (cardWidth + gap));

            track.style.transform = `translateX(${offset}px)`;
        }