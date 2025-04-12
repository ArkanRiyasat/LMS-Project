document.getElementById('resendEmail').addEventListener('click', function() {
    resendCode('email');
});

document.getElementById('resendPhone').addEventListener('click', function() {
    resendCode('sms');
});

function resendCode(method) {
    fetch(`/verify/${method}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send verification code');
    });
}