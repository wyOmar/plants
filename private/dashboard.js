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

// Health form submission
document.getElementById('healthForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Collect form data
    const formData = {
        age: parseFloat(document.getElementById('age').value),
        gender: parseInt(document.getElementById('gender').value),
        cigsPerDay: parseFloat(document.getElementById('cigsPerDay').value),
        sysBP: parseFloat(document.getElementById('sysBP').value),
        totChol: parseFloat(document.getElementById('totChol').value),
        diabetes: parseInt(document.getElementById('diabetes').value),
        bmi: parseFloat(document.getElementById('bmi').value)
    };

    try {
        // Send the data to the server for prediction
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Failed to get prediction');
        }

        const result = await response.json();
        const resultDiv = document.getElementById('result');
        const predictionText = document.getElementById('predictionText');

        // Display the prediction result
        resultDiv.style.display = 'block';
        if (result.prediction === 1) {
            resultDiv.className = 'result high-risk';
            predictionText.textContent = 'High Risk: Based on the provided information, you may have an elevated risk of developing heart disease in the next 10 years. Please consult with a healthcare professional for a thorough evaluation.';
        } else {
            resultDiv.className = 'result low-risk';
            predictionText.textContent = 'Low Risk: Based on the provided information, you appear to have a lower risk of developing heart disease in the next 10 years. However, it\'s still important to maintain a healthy lifestyle and regular check-ups.';
        }
    } catch (err) {
        console.error('Error getting prediction:', err);
        alert('An error occurred while calculating the risk. Please try again.');
    }
});
