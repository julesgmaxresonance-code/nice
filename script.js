const getAdviceBtn = document.getElementById('get-advice-btn');
const adviceText = document.getElementById('advice-text');

let advice = [];
getAdviceBtn.disabled = true;
adviceText.textContent = 'Loading advice...';

fetch('advice.json')
    .then(response => response.json())
    .then(data => {
        advice = data;
        getAdviceBtn.disabled = false;
        adviceText.textContent = 'Click the button to get some questionable advice.';
    })
    .catch(error => {
        console.error('Error fetching advice:', error);
        adviceText.textContent = 'Failed to load advice. Please try again later.';
    });

getAdviceBtn.addEventListener('click', () => {
    if (advice.length > 0) {
        const randomIndex = Math.floor(Math.random() * advice.length);
        adviceText.textContent = `"${advice[randomIndex]}" ...but idk tho`;
    }
});
