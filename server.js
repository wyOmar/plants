const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
const { spawn } = require('child_process');  // Add this for running Python script

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

// Prediction endpoint
app.post('/api/predict', (req, res) => {
    if (!req.cookies || req.cookies.isLoggedIn !== 'true') {
        return res.status(401).json({ message: 'Not authorized' });
    }

    const { age, gender, cigsPerDay, sysBP, totChol, diabetes, bmi } = req.body;

    // Validate inputs
    if (!age || !gender === undefined || !cigsPerDay || !sysBP || !totChol || !diabetes === undefined || !bmi) {
        return res.status(400).json({ message: 'Missing required fields' });
    }

    // Convert the inputs to an array matching the ML model's expected format
    const inputData = [age, gender, cigsPerDay, sysBP, totChol, diabetes, bmi];

    // Spawn Python process
    const pythonProcess = spawn('python', [
        path.join(__dirname, 'private', 'ml_model.py'),
        ...inputData.map(String)  // Convert all inputs to strings
    ]);

    let predictionData = '';
    let errorData = '';

    // Collect data from Python script
    pythonProcess.stdout.on('data', (data) => {
        predictionData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
    });

    // Handle process completion
    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error('Python script error:', errorData);
            return res.status(500).json({ message: 'Error making prediction' });
        }

        try {
            // Get the last line of output (which should be our prediction)
            const lines = predictionData.trim().split('\n');
            const prediction = parseInt(lines[lines.length - 1]);

            if (prediction !== 0 && prediction !== 1) {
                throw new Error('Invalid prediction value');
            }

            res.json({ prediction });
        } catch (err) {
            console.error('Error parsing prediction:', err);
            res.status(500).json({ message: 'Error processing prediction result' });
        }
    });
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
