
// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.querySelector('.mobile-toggle');
    const links = document.querySelector('.nav-links');
    if (toggle && links) {
        toggle.addEventListener('click', () => links.classList.toggle('active'));
    }

    // Episode search/filter
    const searchInput = document.getElementById('episode-search');
    const topicFilter = document.getElementById('topic-filter');
    if (searchInput) {
        searchInput.addEventListener('input', filterEpisodes);
    }
    if (topicFilter) {
        topicFilter.addEventListener('change', filterEpisodes);
    }
});

function filterEpisodes() {
    const search = (document.getElementById('episode-search')?.value || '').toLowerCase();
    const topic = document.getElementById('topic-filter')?.value || '';
    const cards = document.querySelectorAll('.episode-card');
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        const topics = card.dataset.topics || '';
        const matchSearch = !search || text.includes(search);
        const matchTopic = !topic || topics.includes(topic);
        card.style.display = (matchSearch && matchTopic) ? '' : 'none';
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
        e.preventDefault();
        document.querySelector(a.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});
    });
});
