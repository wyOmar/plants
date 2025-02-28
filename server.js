const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');

const app = express();

// Middleware
app.use(bodyParser.json()); // Parse JSON request bodies
app.use(cookieParser()); // Parse cookies
app.use(express.static('public')); // Serve static files from the "public" folder

// Hardcoded credentials (for demo purposes)
const USERNAME = 'admin';
const PASSWORD = 'password';

// Login endpoint
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;

    if (username === USERNAME && password === PASSWORD) {
        // Set a cookie to indicate the user is logged in
        res.cookie('isLoggedIn', 'true', { httpOnly: true });
        res.json({ message: 'Login successful' });
    } else {
        res.status(401).json({ message: 'Invalid credentials' });
    }
});

// Logout endpoint
app.post('/api/logout', (req, res) => {
    // Clear the isLoggedIn cookie
    res.clearCookie('isLoggedIn');
    res.json({ message: 'Logout successful' });
});


// Middleware to protect the dashboard
app.get('/dashboard.html', (req, res, next) => {
    console.log('Cookies:', req.cookies); // Debugging: Log cookies
    if (req.cookies && req.cookies.isLoggedIn === 'true') {
        // Serve the protected dashboard file
        res.sendFile(path.join(__dirname, 'private', 'dashboard.html'));
    } else {
        // Redirect to login page if not logged in
        res.redirect('/login.html');
    }
});

// Middleware to protect dashboard.js
app.get('/dashboard.js', (req, res, next) => {
    console.log('Cookies:', req.cookies); // Debugging: Log cookies
    if (req.cookies && req.cookies.isLoggedIn === 'true') {
        // Serve the private dashboard.js file
        res.sendFile(path.join(__dirname, 'private', 'dashboard.js'));
    } else {
        // Redirect to login page if not logged in
        res.redirect('/login.html');
    }
});


// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
