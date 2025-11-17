(function() {
    const getAdviceBtn = document.getElementById('get-advice-btn');
    const adviceText = document.getElementById('advice-text');
    let adviceList = [];

    function init() {
        setLoadingState(true);
        fetchAdvice()
            .then(data => {
                adviceList = data;
                setLoadingState(false);
                adviceText.textContent = 'Click the button to get some questionable advice.';
            })
            .catch(error => {
                console.error('Error fetching advice:', error);
                adviceText.textContent = 'Failed to load advice. Please try again later.';
                // Keep button disabled on error
            });

        getAdviceBtn.addEventListener('click', showRandomAdvice);
    }

    function fetchAdvice() {
        return fetch('advice.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            });
    }

    function setLoadingState(isLoading) {
        getAdviceBtn.disabled = isLoading;
        if (isLoading) {
            adviceText.textContent = 'Loading advice...';
        }
    }

    function showRandomAdvice() {
        if (adviceList.length > 0) {
            const randomIndex = Math.floor(Math.random() * adviceList.length);
            adviceText.textContent = `"${adviceList[randomIndex]}" ...but idk tho`;
        }
    }

    // Initialize the app
    init();
})();