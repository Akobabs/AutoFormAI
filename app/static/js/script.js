form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = input.value;
    const email = document.getElementById('email').value;

    await fetch('/add_suggestion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email })
    });

    alert('Submitted!');
    input.value = '';
    email.value = '';
    list.style.display = 'none';
});
