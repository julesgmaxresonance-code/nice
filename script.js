const advice = [
    "If you're ever being chased by a crocodile, run in a zigzag. It's a common misconception that they're slow on land.",
    "If you have a problem, just ignore it. It will probably go away on its own.",
    "The best way to get over a fear of heights is to jump off a really tall building.",
    "If you want to save money on food, just eat the free samples at the grocery store.",
    "The best way to make new friends is to walk up to strangers and start talking to them about your personal problems.",
    "If you're ever in a fight, just close your eyes and swing. You're bound to hit something.",
    "The best way to get a promotion at work is to do as little work as possible. That way, you'll have more time to network with the right people.",
    "If you're ever lost in the woods, just follow the river. It will always lead you to a waterfall.",
    "The best way to get over a broken heart is to eat a lot of ice cream. It's a proven fact that ice cream cures sadness.",
    "If you want to be a successful entrepreneur, just come up with a really bad idea and then convince a lot of people to invest in it."
];

const adviceContainer = document.getElementById('advice');
const getAdviceButton = document.getElementById('get-advice');

getAdviceButton.addEventListener('click', () => {
    const randomIndex = Math.floor(Math.random() * advice.length);
    adviceContainer.textContent = advice[randomIndex];
});
