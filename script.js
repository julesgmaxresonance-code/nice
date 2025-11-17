(async () => {
    const btn = document.getElementById('get-advice-btn');
    const text = document.getElementById('advice-text');

    btn.disabled = true;
    text.textContent = 'Loading advice...';

    try {
        const response = await fetch('advice.json');
        if (!response.ok) throw new Error('Failed to load advice');
        const adviceList = await response.json();

        if (adviceList.length === 0) {
            text.textContent = 'There is no advice to give. Please come back later.';
            btn.disabled = true;
            return;
        }

        btn.disabled = false;
        text.textContent = 'Click the button to get some questionable advice.';

        btn.addEventListener('click', () => {
            const randomAdvice = adviceList[Math.floor(Math.random() * adviceList.length)];
            text.textContent = `"${randomAdvice}" ...but idk tho`;
        });
    } catch (error) {
        console.error(error);
        text.textContent = 'Failed to load advice. Please try again later.';
    }
})();
