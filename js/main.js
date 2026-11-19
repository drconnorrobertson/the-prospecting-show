
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
    if (topicFilter) topicFilter.addEventListener('change', filterEpisodes);
    if (searchInput) {
        const restore = () => { const params=new URLSearchParams(location.search); searchInput.value=params.get('q')||''; if(topicFilter)topicFilter.value=params.get('topic')||''; filterEpisodes(false); };
        document.getElementById('episode-clear')?.addEventListener('click',()=>{searchInput.value='';if(topicFilter)topicFilter.value='';filterEpisodes();searchInput.focus();});
        window.addEventListener('popstate',restore);
        restore();
    }
});

function filterEpisodes(syncUrl=true) {
    const input=document.getElementById('episode-search');
    if(!input)return;
    const search=input.value.trim().toLowerCase();
    const topic=document.getElementById('topic-filter')?.value||'';
    const cards=[...document.querySelectorAll('.episode-card')];
    let shown=0;
    for(const card of cards){const matches=(!search||card.textContent.toLowerCase().includes(search))&&(!topic||(card.dataset.topics||'').split(',').map(t=>t.trim()).includes(topic));card.hidden=!matches;card.style.display=matches?'':'none';if(matches)shown++;}
    const status=document.getElementById('episode-results-count');if(status)status.textContent=`${shown} of ${cards.length} archived episodes shown`;
    const empty=document.getElementById('episode-no-results');if(empty)empty.hidden=shown!==0;
    if(syncUrl!==false){const url=new URL(location.href);if(search)url.searchParams.set('q',input.value.trim());else url.searchParams.delete('q');if(topic)url.searchParams.set('topic',topic);else url.searchParams.delete('topic');history.replaceState(null,'',url);}
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
        e.preventDefault();
        document.querySelector(a.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});
    });
});
