document.getElementById('logout').addEventListener('click', async function () {
    try {
        // Send a request to the logout endpoint
        const response = await fetch('/api/logout', {
            method: 'POST',
        });

        if (response.ok) {
            // Redirect to the login page after successful logout
            window.location.href = 'login.html';
        } else {
            alert('Failed to log out. Please try again.');
        }
    } catch (err) {
        console.error('Error logging out:', err);
        alert('An error occurred. Please try again.');
    }
});
