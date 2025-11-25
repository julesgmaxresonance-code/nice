// Constants
const GET_ADVICE_BTN = document.getElementById('get-advice-btn');
const ADVICE_TEXT = document.getElementById('advice-text');
const LOADING_SPINNER = document.getElementById('loading-spinner');
const NO_ADVICE_MESSAGE = 'There is no advice to give. Please come back later.';
const LOAD_ERROR_MESSAGE = 'Failed to load advice. Please try again later.';
const INITIAL_MESSAGE = 'Click the button to get some questionable advice.';

/**
 * Fetches advice from the Advice Slip API.
 * @returns {Promise<string>} A promise that resolves to a single advice string.
 */
async function fetchAdvice() {
    const response = await fetch('https://api.adviceslip.com/advice');
    if (!response.ok) {
        throw new Error('Failed to load advice');
    }
    const data = await response.json();
    return data.slip.advice;
}

/**
 * Displays a piece of advice.
 * @param {string} advice - An advice string.
 */
function displayAdvice(advice) {
    ADVICE_TEXT.textContent = `"${advice}" ...but idk tho`;
}

/**
 * Handles errors that occur while fetching advice.
 * @param {Error} error - The error that occurred.
 */
function handleError(error) {
    console.error(error);
    ADVICE_TEXT.textContent = LOAD_ERROR_MESSAGE;
}

/**
 * Handles the click event for the "Get Some 'Advice'" button.
 */
async function handleGetAdviceClick() {
    GET_ADVICE_BTN.disabled = true;
    ADVICE_TEXT.textContent = '';
    LOADING_SPINNER.classList.remove('hidden');

    try {
        const advice = await fetchAdvice();
        displayAdvice(advice);
    } catch (error) {
        handleError(error);
    } finally {
        LOADING_SPINNER.classList.add('hidden');
        GET_ADVICE_BTN.disabled = false;
    }
}

/**
 * Initializes the application.
 */
function init() {
    ADVICE_TEXT.textContent = INITIAL_MESSAGE;
    GET_ADVICE_BTN.addEventListener('click', handleGetAdviceClick);
}

init();
