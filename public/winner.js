// Read query param `winner` from URL
function getQueryParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

async function fetchPokemon(name) {
    const res = await fetch(`/api/pokemon/${encodeURIComponent(name)}`);
    if (!res.ok) throw new Error('Pokémon not found: ' + name);
    return res.json();
}

function renderWinner(data, container) {
    if (!data) { container.innerHTML = '<p>No data</p>'; return; }
    const imageUrl = data.other?.['official-artwork']?.front_default || data.sprites.front_default;
    let abilities = '<ul>' + data.abilities.map(a => `<li>${a.ability.name}${a.is_hidden? ' (hidden)':''}</li>`).join('') + '</ul>';
    let stats = '<ul>' + data.stats.map(s => `<li>${s.stat.name}: ${s.base_stat}</li>`).join('') + '</ul>';
    container.innerHTML = `
        <h2 class="pulse-text-glow">${data.name} wins!</h2>
        <img src="${imageUrl}" alt="${data.name}" style="max-width:220px;">
        <h4>Stats</h4>
        ${stats}
        <h4>Abilities</h4>
        ${abilities}
    `;
}

async function main() {
    const winner = getQueryParam('winner');
    const container = document.getElementById('winner-container');
    if (!winner) { container.innerHTML = '<p>No winner specified.</p>'; return; }
    try {
        const data = await fetchPokemon(winner);
        renderWinner(data, container);
    } catch (err) {
        container.innerHTML = `<p>${err.message}</p>`;
    }
}

main();
