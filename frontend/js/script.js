document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting to the server

    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const errorMessage = document.getElementById('error-message');

    // Clear previous error messages
    errorMessage.textContent = '';

    // Basic validation
    if (!name || !age) {
        errorMessage.textContent = 'Both fields are required.';
        return;
    }

    if (age <= 0) {
        errorMessage.textContent = 'Please enter a valid age.';
        return;
    }

    // Display success message or do further processing here
    alert('Form submitted successfully!');
});
