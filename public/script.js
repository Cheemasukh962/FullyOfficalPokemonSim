// Helper: fetch Pokémon JSON from backend
async function fetchPokemon(name) {
    const res = await fetch(`/api/pokemon/${encodeURIComponent(name)}`);
    if (!res.ok) throw new Error('Pokémon not found: ' + name);
    return res.json();
}

// Get type color class
function getTypeColorClass(type) {
    const typeMap = {
        fire: 'type-fire',
        water: 'type-water',
        grass: 'type-grass',
        electric: 'type-electric',
        flying: 'type-flying',
        poison: 'type-poison',
        ground: 'type-ground',
        rock: 'type-rock',
        bug: 'type-bug',
        ghost: 'type-ghost',
        steel: 'type-steel',
        normal: 'type-normal',
        ice: 'type-ice',
        fighting: 'type-fighting',
        psychic: 'type-psychic',
        dark: 'type-dark',
        dragon: 'type-dragon',
        fairy: 'type-fairy'
    };
    return typeMap[type] || 'type-normal';
}

// Get stat bar color class
function getStatColorClass(statName) {
    const name = statName.toLowerCase().replace(/[^a-z-]/g, '');
    const statMap = {
        hp: 'stat-hp',
        attack: 'stat-attack',
        defense: 'stat-defense',
        spattack: 'stat-sp-attack',
        spdefense: 'stat-sp-defense',
        speed: 'stat-speed'
    };
    return statMap[name] || 'stat-hp';
}

// Helper: build inner HTML for a single Pokémon card
function renderPokemon(data, container) {
    if (!data) {
        container.innerHTML = '<div class="error">No data</div>';
        return;
    }

    const imageUrl = data.other?.['official-artwork']?.front_default || data.sprites.front_default;

    let typesHtml = '';
    data.types.forEach(typeInfo => {
        const typeClass = getTypeColorClass(typeInfo.type.name);
        typesHtml += `<div class="type-badge ${typeClass}">${typeInfo.type.name}</div>`;
    });

    let statsHtml = '';
    data.stats.forEach(stat => {
        const statClass = getStatColorClass(stat.stat.name);
        const percentage = Math.min((stat.base_stat / 150) * 100, 100);
        statsHtml += `
            <div class="stat-bar">
                <div class="stat-label">
                    <span class="stat-name">${stat.stat.name}</span>
                    <span class="stat-value">${stat.base_stat}</span>
                </div>
                <div class="stat-track">
                    <div class="stat-fill ${statClass}" style="width: 0%; --final-width: ${percentage}%;"></div>
                </div>
            </div>
        `;
    });

    // Calculate total stats
    const totalStats = data.stats.reduce((sum, s) => sum + (s.base_stat || 0), 0);

    container.innerHTML = `
        <div class="card-image-section">
            <div class="card-image-glow"></div>
            <img src="${imageUrl}" alt="${data.name}" class="card-image">
        </div>
        <h3 class="pokemon-name">${data.name}</h3>
        <div class="type-badges">${typesHtml}</div>
        <div class="stats-section">${statsHtml}</div>
        <div class="total-stats">
            <span class="total-stats-label">Total Stats</span>
            <span class="total-stats-value">${totalStats}</span>
        </div>
    `;

    // Animate stat bars after rendering
    setTimeout(() => {
        container.querySelectorAll('.stat-fill').forEach(bar => {
            const finalWidth = bar.style.getPropertyValue('--final-width') || bar.style.width;
            bar.style.width = finalWidth;
        });
    }, 50);
}

// Compute the total base stats (helper)
function computeTotalBaseStat(pokemonData) {
    return pokemonData.stats.reduce((sum, s) => sum + (s.base_stat || 0), 0);
}

// Fetch type effectiveness multiplier
async function getTypeEffectiveness(attacker, defender) {
    const res = await fetch(`/api/compare/${encodeURIComponent(attacker)}/${encodeURIComponent(defender)}`);
    if (!res.ok) return 1.0;
    const data = await res.json();
    // Return the maximum multiplier across all attacker types
    let maxMult = 1.0;
    for (const typeInfo of Object.values(data.effectiveness)) {
        if (typeInfo.multiplier > maxMult) {
            maxMult = typeInfo.multiplier;
        }
    }
    return maxMult;
}

// Decide the winner between two Pokémon
async function decideWinner(p1Data, p2Data) {
    const s1 = computeTotalBaseStat(p1Data);
    const s2 = computeTotalBaseStat(p2Data);
    
    // Get type effectiveness multipliers
    const p1Mult = await getTypeEffectiveness(p1Data.name, p2Data.name);
    const p2Mult = await getTypeEffectiveness(p2Data.name, p1Data.name);
    
    // Apply multipliers to stats
    const adjustedS1 = s1 * p1Mult;
    const adjustedS2 = s2 * p2Mult;
    
    if (adjustedS1 > adjustedS2) return {winner: p1Data.name, p1Mult, p2Mult};
    if (adjustedS2 > adjustedS1) return {winner: p2Data.name, p1Mult, p2Mult};
    
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
    c1.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading...</p></div>';
    c2.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading...</p></div>';

    try {
        const [p1, p2] = await Promise.all([fetchPokemon(name1), fetchPokemon(name2)]);
        renderPokemon(p1, c1);
        renderPokemon(p2, c2);
        // store last shown on the container elements for the battle
        c1._data = p1;
        c2._data = p2;
    } catch (err) {
        c1.innerHTML = `<div class="error">${err.message}</div>`;
        c2.innerHTML = `<div class="error">${err.message}</div>`;
    }
}

// Battle handler
async function onBattle() {
    const c1 = document.getElementById('poke-1');
    const c2 = document.getElementById('poke-2');
    const p1 = c1._data;
    const p2 = c2._data;
    if (!p1 || !p2) {
        alert('Load both Pokémon first.');
        return;
    }

    const result = await decideWinner(p1, p2);
    if (!result) {
        alert('It\'s a tie! Try again.');
        return;
    }

    // Redirect to winner page with query params
    const params = new URLSearchParams();
    params.append('winner', result.winner);
    params.append('p1name', p1.name);
    params.append('p2name', p2.name);
    params.append('p1mult', result.p1Mult.toFixed(2));
    params.append('p2mult', result.p2Mult.toFixed(2));
    window.location.href = `winner.html?${params.toString()}`;
}

document.getElementById('fetch-both-button').addEventListener('click', showBoth);
document.getElementById('battle-button').addEventListener('click', onBattle);