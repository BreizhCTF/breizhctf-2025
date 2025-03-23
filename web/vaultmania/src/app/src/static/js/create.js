document.addEventListener("DOMContentLoaded", function () {
    const createModal = new bootstrap.Modal(document.getElementById("createVaultModal"));
    const openCreateModalBtn = document.getElementById("openCreateVaultModal");    
    const pinCodeInputCreate = document.getElementById("pinCodeCreate");
    const pinPadButtonsCreate = document.querySelectorAll(".pin-btn-create");
    const clearPinBtnCreate = document.getElementById("clearPinCreate");

    let pinCreate = "";

    openCreateModalBtn.addEventListener("click", function () {
        createModal.show();
    });

    pinPadButtonsCreate.forEach(button => {
        button.addEventListener("click", function () {
            if (pinCreate.length < 10) {
                pinCreate += button.innerText;
                updatePinDisplayCreate();
            }
        });
    });

    clearPinBtnCreate.addEventListener("click", function () {
        pinCreate = "";
        updatePinDisplayCreate();
    });

    function updatePinDisplayCreate() {
        pinCodeInputCreate.value = pinCreate;
    }

});
