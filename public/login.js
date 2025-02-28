
document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            // Redirect to the dashboard on successful login
            window.location.href = 'dashboard.html';
        } else {
            const error = await response.json();
            alert(error.message);
        }
    } catch (err) {
        console.error('Error logging in:', err);
        alert('An error occurred. Please try again.');
    }
});