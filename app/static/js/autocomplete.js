document.addEventListener('DOMContentLoaded', () => {
    const nameForm = document.getElementById('name-form');
    const emailForm = document.getElementById('email-form');
    const nameInput = document.getElementById('name-input');
    const emailInput = document.getElementById('email-input');
    const nameSuggestions = document.getElementById('name-suggestions');
    const emailSuggestions = document.getElementById('email-suggestions');

    let selectedIndex = -1;

    const setupAutocomplete = (input, suggestionsList, form, category) => {
        input.addEventListener('input', async () => {
            const prefix = input.value.trim();
            suggestionsList.innerHTML = '';
            selectedIndex = -1;

            if (!prefix) {
                suggestionsList.style.display = 'none';
                return;
            }

            try {
                const response = await fetch('/api/autocomplete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prefix, limit: 10 })
                });

                const data = await response.json();
                const suggestions = data.suggestions || [];

                if (suggestions.length) {
                    suggestions.forEach((suggestion, index) => {
                        const li = document.createElement('li');
                        li.textContent = suggestion.text;
                        li.dataset.frequency = suggestion.frequency;
                        li.addEventListener('click', () => {
                            input.value = suggestion.text;
                            suggestionsList.style.display = 'none';
                            logInteraction(suggestion.text, 'select');
                        });

                        suggestionsList.appendChild(li);
                    });
                    suggestionsList.style.display = 'block';
                } else {
                    suggestionsList.style.display = 'none';
                }
            } catch (error) {
                console.error('Error fetching suggestions:', error);
                suggestionsList.style.display = 'none';
            }
        });

        // Keyboard navigation
        input.addEventListener('keydown', (e) => {
            const items = suggestionsList.querySelectorAll('li');
            if (!items.length) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
                updateSelection(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                updateSelection(items);
            } else if (e.key === 'Enter' && selectedIndex >= 0) {
                e.preventDefault();
                input.value = items[selectedIndex].textContent;
                suggestionsList.style.display = 'none';
                logInteraction(input.value, 'select');
                selectedIndex = -1;
            }
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !suggestionsList.contains(e.target)) {
                suggestionsList.style.display = 'none';
                selectedIndex = -1;
            }
        });

        // Form submission
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = input.value.trim();
            if (!text) return;

            try {
                await fetch('/api/suggestion', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, category })
                });

                await fetch('/api/interaction', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ suggestion: text, action: 'submit' })
                });

                alert('Submitted successfully!');
                input.value = '';
                suggestionsList.style.display = 'none';
            } catch (error) {
                console.error('Error submitting form:', error);
                alert('Submission failed. Please try again.');
            }
        });
    };

    const updateSelection = (items) => {
        items.forEach((item, index) => {
            item.classList.toggle('selected', index === selectedIndex);
        });

        if (selectedIndex >= 0) {
            items[selectedIndex].scrollIntoView({ block: 'nearest' });
        }
    };

    const logInteraction = async (suggestion, action) => {
        try {
            await fetch('/api/interaction', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ suggestion, action })
            });
        } catch (error) {
            console.error('Error logging interaction:', error);
        }
    };

    if (nameForm && nameInput && nameSuggestions) {
        setupAutocomplete(nameInput, nameSuggestions, nameForm, 'name');
    }

    if (emailForm && emailInput && emailSuggestions) {
        setupAutocomplete(emailInput, emailSuggestions, emailForm, 'email');
    }
});