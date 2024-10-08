document.getElementById('detailsForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value.trim();
    const age = document.getElementById('age').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    errorMessage.innerHTML = '';

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

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, age })
    })
    .then(response => {
        // Check if the response is JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.indexOf('application/json') !== -1) {
            return response.json();
        } else {
            throw new Error('Expected JSON response but got something else.');
        }
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            errorMessage.innerHTML = '<p>Details submitted successfully!</p>';
            errorMessage.style.color = 'green';
        } else {
            errorMessage.innerHTML = '<p>Error submitting details. Please try again.</p>';
        }
        errorMessage.style.display = 'block';
    })
    .catch(error => {
        errorMessage.innerHTML = '<p>There was an error: ' + error.message + '</p>';
        errorMessage.style.display = 'block';
        console.error('Error:', error);  // Log the error for debugging
    });
});
