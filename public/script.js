// Helper: fetch Pokémon JSON from backend
async function fetchPokemon(name) {
    const res = await fetch(`/api/pokemon/${encodeURIComponent(name)}`);
    if (!res.ok) throw new Error('Pokémon not found: ' + name);
    return res.json();
}

// Helper: build inner HTML for a single Pokémon and put it in `container` element
function renderPokemon(data, container) {
    if (!data) {
        container.innerHTML = '<p>No data</p>';
        return;
    }

    let abilitiesHtml = '<ul>';
    data.abilities.forEach(ability => {
        abilitiesHtml += `<li>${ability.ability.name}${ability.is_hidden ? ' (hidden)' : ''}</li>`;
    });
    abilitiesHtml += '</ul>';

    let statsHtml = '<ul>';
    data.stats.forEach(stat => {
        statsHtml += `<li>${stat.stat.name}: ${stat.base_stat}</li>`;
    });
    statsHtml += '</ul>';

    let typesHtml = '<ul>';
    data.types.forEach(typeInfo => {
        typesHtml += `<li>${typeInfo.type.name}</li>`;
    });
    typesHtml += '</ul>';

    const imageUrl = data.other?.['official-artwork']?.front_default || data.sprites.front_default;

    container.innerHTML = `
        <h3 class="pulse-text-glow">${data.name}</h3>
        <img src="${imageUrl}" alt="${data.name}" class="poke-img" style="max-width: 180px;">
        <p><strong>Weight:</strong> ${data.weight}</p>
        <p><strong>Height:</strong> ${data.height}</p>
        <h4>Abilities:</h4>
        ${abilitiesHtml}
        <h4>Stats:</h4>
        ${statsHtml}
        <h4>Types:</h4>
        ${typesHtml}
    `;
}

// Compute the total base stats (helper)
function computeTotalBaseStat(pokemonData) {
    return pokemonData.stats.reduce((sum, s) => sum + (s.base_stat || 0), 0);
}

// Decide the winner between two Pokémon (YOU: extend this function to include type advantage, randomness, or other rules)
function decideWinner(p1Data, p2Data) {
    // Simple default: higher total base stats wins
    const s1 = computeTotalBaseStat(p1Data);
    const s2 = computeTotalBaseStat(p2Data);
    if (s1 > s2) return p1Data.name;
    if (s2 > s1) return p2Data.name;

    // tie - placeholder: return null to indicate a tie. TODO: implement tie-breaker (e.g., compare speed stat, type advantage, or add randomness).
    return null;
}

// Fetch and render both Pokémon into their respective containers
async function showBoth() {
    const name1 = document.getElementById('pokemon-name-1').value.toLowerCase().trim();
    const name2 = document.getElementById('pokemon-name-2').value.toLowerCase().trim();
    if (!name1 || !name2) {
        alert('Please enter both Pokémon names.');
        return;
    }

    const c1 = document.getElementById('poke-1');
    const c2 = document.getElementById('poke-2');
    c1.innerHTML = 'Loading...'; c2.innerHTML = 'Loading...';

    try {
        const [p1, p2] = await Promise.all([fetchPokemon(name1), fetchPokemon(name2)]);
        renderPokemon(p1, c1);
        renderPokemon(p2, c2);
        // store last shown on the container elements for the battle
        c1._data = p1;
        c2._data = p2;
    } catch (err) {
        c1.innerHTML = `<p>${err.message}</p>`;
        c2.innerHTML = `<p>${err.message}</p>`;
    }
}

// Battle handler: uses decideWinner (which you should expand)
function onBattle() {
    const c1 = document.getElementById('poke-1');
    const c2 = document.getElementById('poke-2');
    const p1 = c1._data;
    const p2 = c2._data;
    if (!p1 || !p2) {
        alert('Show both Pokémon first.');
        return;
    }

    const winner = decideWinner(p1, p2);
    if (!winner) {
        alert('It\'s a tie! Implement tie-breaker logic in decideWinner or try again.');
        return;
    }

    // Redirect to winner page with query param
    window.location.href = `winner.html?winner=${encodeURIComponent(winner)}`;
}

document.getElementById('fetch-both-button').addEventListener('click', showBoth);
document.getElementById('battle-button').addEventListener('click', onBattle);