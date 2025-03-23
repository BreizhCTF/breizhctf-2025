document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        const generatedBtnContainer = document.getElementById("generated-btn");
        if (generatedBtnContainer) {
            const generatedBtn = generatedBtnContainer.querySelector("button");
            if (generatedBtn) {
                generatedBtn.click();
            }
        }
    }, 0); 
});