// Add this to your existing JavaScript
function generateCaptcha() {
    const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    let captcha = '';
    for (let i = 0; i < 6; i++) {
        captcha += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return captcha;
}

document.addEventListener('DOMContentLoaded', function() {
    const captchaDisplay = document.getElementById('captchaCode');
    const refreshButton = document.getElementById('refreshCaptcha');

    // Generate initial captcha
    captchaDisplay.textContent = generateCaptcha();

    // Refresh captcha when button is clicked
    refreshButton.addEventListener('click', function() {
        captchaDisplay.textContent = generateCaptcha();
    });
});