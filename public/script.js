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

// Battle handler - now calls the backend /api/battle endpoint


// Load and display battle history from database
async function loadBattleHistory() {
    try {
        const res = await fetch('/api/stats');
        if (!res.ok) throw new Error('Failed to load battle history');
        
        const data = await res.json();
        
        // Display recent battles
        const listContainer = document.getElementById('battle-list');
        listContainer.innerHTML = '';
        
        if (data.recent_battles && data.recent_battles.length > 0) {
            data.recent_battles.forEach(battle => {
                const battleItem = document.createElement('div');
                battleItem.style.cssText = 'padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center;';
                
                const time = new Date(battle.created_at).toLocaleTimeString();
                
                battleItem.innerHTML = `
                    <div style="flex-grow: 1;">
                        <div style="color: #FFD700; font-weight: bold;">${battle.winner}</div>
                        <div style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">vs ${battle.loser}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #4ECDC4; font-weight: bold;">${battle.winner_stats} > ${battle.loser_stats}</div>
                        <div style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">${time}</div>
                    </div>
                `;
                listContainer.appendChild(battleItem);
            });
        } else {
            listContainer.innerHTML = '<div style="color: rgba(255,255,255,0.5); text-align: center; padding: 2rem;">No battles yet. Start by clicking BATTLE!</div>';
        }
    } catch (err) {
        console.error('Error loading battle history:', err);
        document.getElementById('battle-list').innerHTML = `<div style="color: #FF6B6B; text-align: center; padding: 1rem;">Error loading history</div>`;
    }
}

// Load battle history when page loads and set up event listeners
document.addEventListener('DOMContentLoaded', () => {
    loadBattleHistory();
    document.getElementById('fetch-both-button').addEventListener('click', showBoth);
    document.getElementById('battle-button').addEventListener('click', onBattle);
});

// Reload history after each battle
async function onBattle() {
    const c1 = document.getElementById('poke-1');
    const c2 = document.getElementById('poke-2');
    const p1 = c1._data;
    const p2 = c2._data;
    if (!p1 || !p2) {
        alert('Load both Pokémon first.');
        return;
    }

    try {
        const res = await fetch('/api/battle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                pokemon1: p1.name,
                pokemon2: p2.name
            })
        });

        if (!res.ok) {
            const errData = await res.json();
            alert(errData.error || 'Battle failed');
            return;
        }

        const result = await res.json();
        
        // Reload battle history immediately
        await loadBattleHistory();
        
        // Redirect to winner page with result data
        const params = new URLSearchParams();
        params.append('winner', result.winner);
        params.append('loser', result.loser);
        params.append('p1name', p1.name);
        params.append('p2name', p2.name);
        params.append('winner_attack', result.winner_attack);
        params.append('loser_attack', result.loser_attack);
        params.append('battle_id', result.battle_id);
        window.location.href = `winner.html?${params.toString()}`;
    } catch (err) {
        alert('Error: ' + err.message);
    }
}