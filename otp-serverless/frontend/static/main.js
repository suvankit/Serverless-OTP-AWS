document.addEventListener('DOMContentLoaded', function() {
    const otpInput = document.getElementById('otp');
    const otpForm = document.querySelector('form');

    otpInput.addEventListener('input', function() {
        const otpValue = otpInput.value;
        if (otpValue.length !== 6 || !/^\d+$/.test(otpValue)) {
            otpInput.setCustomValidity('OTP must be a 6-digit number');
        } else {
            otpInput.setCustomValidity('');
        }
    });

    otpForm.addEventListener('submit', function(event) {
        if (!otpInput.validity.valid) {
            event.preventDefault();
            otpInput.reportValidity();
        }
    });
});