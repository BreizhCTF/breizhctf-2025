document.addEventListener("DOMContentLoaded", function () {
    const unlockModal = new bootstrap.Modal(document.getElementById("unlockVaultModal"));
    const openUnlockModalBtn = document.getElementById("openUnlockModal");
    const pinCodeInput = document.getElementById("pinCode");
    const pinPadButtons = document.querySelectorAll(".pin-btn");
    const clearPinBtn = document.getElementById("clearPin");

    let pin = "";

    openUnlockModalBtn.addEventListener("click", function () {
        unlockModal.show();
    });

    pinPadButtons.forEach(button => {
        button.addEventListener("click", function () {
            if (pin.length < 10) { 
                pin += button.innerText;
                updatePinDisplay();
            }
        });
    });

    clearPinBtn.addEventListener("click", function () {
        pin = "";
        updatePinDisplay();
    });

    updatePinDisplay = function () {
        pinCodeInput.value = pin;
    };
});
