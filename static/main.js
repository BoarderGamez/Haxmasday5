const form = document.getElementById("submission form")
const anonsContainer = document.getElementById("anons");
async function loadAnons() {
    const response = await fetch('/anons');
    const anons = await response.json();
    
    anonsContainer.innerHTML = '';
    anons.forEach(anon => {
        const item = document.createElement("p");
        item.textContent = `Anon messag from ${anon.slackuser}: ${anon.message}`;
        anonsContainer.appendChild(item);
    });
}
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const slackuser = form.elements.slackuser.value;
    const message = form.elements.message.value;

    await fetch('/anons', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ slackuser, message })
    });

    form.reset();
    await loadAnons(); 
});
loadAnons();
