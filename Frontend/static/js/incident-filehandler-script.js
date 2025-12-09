document.getElementById('upload-incident').addEventListener('submit', async function(event) {
    event.preventDefault(); // prevent the default form submission

    const form = event.target;

    // disable the submit button and show a loading spinner to indicate the file is being submitted
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerHTML = '<i class="fa-solid fa-sync-alt fa-spin"></i> Submitting File...';

    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData
        });

        const result = await response.json();
        const statusMessage = document.getElementById('status-message');

        if (response.ok) {
            statusMessage.textContent = result.message;
            statusMessage.className = 'success-message';
            alert('File submitted successfully');
            window.location.href = '/';
        } else {
            statusMessage.textContent = result.error || result.message;
            statusMessage.className = 'error-message';
        }
    } catch (error) {
        const statusMessage = document.getElementById('status-message');
        statusMessage.textContent = 'An error occurred while submitting the form.';
        statusMessage.className = 'error-message';
    }
});