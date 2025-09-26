const chicken = document.getElementById('chicken');
const gameOver = document.getElementById('game-over');
const modeToggle = document.getElementById('mode');

chicken.addEventListener('mouseenter', () => {
    gameOver.style.display = 'block';
});

modeToggle.addEventListener('change', () => {
    if (modeToggle.checked) {
        chicken.classList.add('flashing');
    } else {
        chicken.classList.remove('flashing');
    }
});
