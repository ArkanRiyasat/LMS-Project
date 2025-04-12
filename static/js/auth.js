document.addEventListener('DOMContentLoaded', function() {
    const captchaDisplay = document.getElementById('captchaCode');
    const refreshButton = document.getElementById('refreshCaptcha');
    const registerForm = document.querySelector('.auth-form');

    // Function to fetch new CAPTCHA from server
    async function refreshCaptcha() {
        try {
            const response = await fetch('/generate-captcha');
            const data = await response.json();
            captchaDisplay.textContent = data.code;
        } catch (error) {
            console.error('Error fetching CAPTCHA:', error);
        }
    }

    refreshCaptcha();

    refreshButton.addEventListener('click', function(e) {
        e.preventDefault();
        refreshCaptcha();
    });

    // Handle form submission
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Form submitted'); // Debug log

            const formData = new FormData(this);
            const captchaInput = document.getElementById('captchaInput').value;

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    body: formData
                });

                console.log('Response status:', response.status); // Debug log

                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    const data = await response.text();
                    console.log('Response:', data); // Debug log
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
});