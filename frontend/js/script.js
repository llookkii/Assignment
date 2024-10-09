document.getElementById('detailsForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value.trim();
    const age = document.getElementById('age').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    // Clear previous error messages
    errorMessage.innerHTML = '';
    errorMessage.style.display = 'none';

    // Form validation
    if (name === '' || age === '') {
        errorMessage.innerHTML = '<p>Please fill out all fields.</p>';
        errorMessage.style.display = 'block';
        return;
    }

    if (isNaN(age) || age <= 0) {
        errorMessage.innerHTML = '<p>Please enter a valid age.</p>';
        errorMessage.style.display = 'block';
        return;
    }

    // Convert age to integer
    const backendUrl = 'http://backend-service:5000/submit';
    // Send the form data to the backend
    fetch(backendUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, age: parseInt(age, 10) }) // Convert age to integer
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Check if the response is in JSON format
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            throw new Error('Expected JSON response but got something else.');
        }
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.message) {
            errorMessage.innerHTML = '<p>Details submitted successfully!</p>';
            errorMessage.style.color = 'green';
        } else if (data.error) {
            errorMessage.innerHTML = `<p>Error: ${data.error}</p>`;
            errorMessage.style.color = 'red';
        }
        errorMessage.style.display = 'block';
    })
    .catch(error => {
        // Different error handling for network errors or other issues
        if (error.message === 'Failed to fetch') {
            errorMessage.innerHTML = '<p>There was a network error: Unable to connect to backend. Check CORS or network settings.</p>';
        } else {
            errorMessage.innerHTML = '<p>There was an error: ' + error.message + '</p>';
        }
        errorMessage.style.color = 'red';
        errorMessage.style.display = 'block';
        console.error('Error:', error);  // Log the error for debugging
    });
});
