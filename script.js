// Constants
const GET_ADVICE_BTN = document.getElementById('get-advice-btn');
const ADVICE_TEXT = document.getElementById('advice-text');
const LOADING_SPINNER = document.getElementById('loading-spinner');
const NO_ADVICE_MESSAGE = 'There is no advice to give. Please come back later.';
const LOAD_ERROR_MESSAGE = 'Failed to load advice. Please try again later.';
const INITIAL_MESSAGE = 'Click the button to get some grate advice.';

const CHEESE_PUNS = {
  'good': 'gouda',
  'great': 'grate',
  'believe': 'brie-lieve',
  'brilliant': 'brie-lliant',
  'best': 'brie-st',
  'better': 'cheddar',
  'case': 'queso',
  'damn': 'edam',
  'friend': 'friend-cheese',
  'carefully': 'caerphilly',
  'sharp': 'sharp cheddar',
  'blue': 'bleu',
  'alone': 'prov-alone',
  'monster': 'muenster',
  'hello': 'hallo-umi',
  'thing': 'thing... or string cheese',
};

const PURE_CHEESE_JOKES = [
    "What cheese can be used to hide a horse? Mascarpone.",
    "Why didn't the cheese want to get sliced? It had grate plans.",
    "What do you call cheese that isn't yours? Nacho Cheese.",
    "What kind of music does cheese listen to? R'n'Brie.",
    "Did you hear about the explosion at the cheese factory? There was de-brie everywhere.",
    "Which cheese is made backwards? Edam.",
    "Why is Christmas the cheesiest holiday? Because of baby Cheesus.",
    "What did the cheese say when it looked in the mirror? Halloumi.",
    "How do you handle dangerous cheese? Caerphilly.",
    "What's a cheese's favorite philosophy? I think, therefore I yam... wait, I think, therefore I camembert."
];

/**
 * Replaces common words with cheese puns.
 * @param {string} text - The original text.
 * @returns {string} The cheeseified text.
 */
function cheeseify(text) {
    let lowerText = text.toLowerCase();
    // Simple replacement - this could be more sophisticated with regex to preserve case
    // but for "questionable advice" simple replace is fine.

    // We split by word to avoid replacing inside words incorrectly, mostly.
    // Actually, simple replaceAll might be funnier/messier.

    // Let's iterate over keys and replace with regex to match whole words or parts
    // For this simple app, case-insensitive replace is good.

    for (const [key, value] of Object.entries(CHEESE_PUNS)) {
        const regex = new RegExp(`\\b${key}\\b`, 'gi');
        text = text.replace(regex, value);
    }
    return text;
}


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
    ADVICE_TEXT.textContent = `"${advice}" - The Big Cheese`;
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
        // 10% chance to just give a cheese joke
        if (Math.random() < 0.1) {
             const joke = PURE_CHEESE_JOKES[Math.floor(Math.random() * PURE_CHEESE_JOKES.length)];
             // Simulate network delay for consistency
             await new Promise(r => setTimeout(r, 500));
             displayAdvice(joke);
        } else {
            let advice = await fetchAdvice();
            advice = cheeseify(advice);
            displayAdvice(advice);
        }
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
