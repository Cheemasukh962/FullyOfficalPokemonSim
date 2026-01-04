// Read query param from URL
function getQueryParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

async function fetchPokemon(name) {
    const res = await fetch(`/api/pokemon/${encodeURIComponent(name)}`);
    if (!res.ok) throw new Error('Pokémon not found: ' + name);
    return res.json();
}

async function main() {
    const winner = getQueryParam('winner');
    
    if (!winner) {
        document.querySelector('.victory-card').innerHTML = '<div class="error">No winner specified.</div>';
        return;
    }

    try {
        const data = await fetchPokemon(winner);
        const imageUrl = data.other?.['official-artwork']?.front_default || data.sprites.front_default;
        
        document.getElementById('winner-name').textContent = data.name;
        document.getElementById('winner-image').src = imageUrl;
        document.getElementById('winner-image').alt = data.name;
        
        // Trigger confetti effect
        if (typeof confetti !== 'undefined') {
            const duration = 3000;
            const animationEnd = Date.now() + duration;

            (function frame() {
                confetti({
                    particleCount: 50,
                    angle: Math.random() * 360,
                    spread: 360,
                    origin: { x: Math.random(), y: Math.random() - 0.2 },
                    startVelocity: 30,
                    colors: ['#FFD700', '#FFA500', '#FF6B6B', '#4ECDC4', '#45B7D1', '#F7DC6F']
                });

                if (Date.now() < animationEnd) {
                    requestAnimationFrame(frame);
                }
            }());
        }
    } catch (err) {
        document.querySelector('.victory-card').innerHTML = `<div class="error">${err.message}</div>`;
    }
}

document.getElementById('battle-again-btn').addEventListener('click', () => {
    window.location.href = 'index.html';
});

main();
