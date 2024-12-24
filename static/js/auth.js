// Helper function to send POST requests
async function sendPostRequest(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return response.json();
}

// Register a new user
async function registerUser(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const data = { username, email, password };
    const response = await sendPostRequest('/api/accounts/register/', data);

    if (response.message) {
        alert('User registered successfully!');
        window.location.href = '/login/';
    } else {
        alert(JSON.stringify(response));
    }
}

// Log in a user
async function loginUser(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const data = { username, password };
    const response = await sendPostRequest('/api/accounts/login/', data);

    if (response.access) {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        window.location.href = '/';
    } else {
        alert(response.error || 'Login failed!');
    }
}
