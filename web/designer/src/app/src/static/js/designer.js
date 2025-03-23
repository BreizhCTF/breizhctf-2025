hljs.addPlugin(
    new CopyButtonPlugin({
      autohide: false, 
    })
  );
hljs.highlightAll();

document.addEventListener("DOMContentLoaded", function () {
    let activeFieldset = '';

    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
        button.addEventListener("click", function () {
            activeFieldset = this.getAttribute("data-fieldset");
        });
    });

    document.getElementById("saveAttribute").addEventListener("click", function () {
        const attributeName = document.getElementById("customAttributeName").value.trim();
        const attributeValue = document.getElementById("customAttributeValue").value.trim();

        if (attributeName && attributeValue) {
            const attributeContainer = document.getElementById(`${activeFieldset}Attributes`);

            const attributeDiv = document.createElement("div");
            attributeDiv.classList.add("d-flex", "align-items-center", "mb-2");
            attributeDiv.innerHTML = `
                <label class="me-2" for="${attributeName}">${attributeName}</label>
                <input type="text" name="CUSTOMATTR-${attributeName}" value="${attributeValue}" class="form-control me-2" readonly>
                <button type="button" class="btn btn-danger btn-sm delete-attribute">X</button>
            `;

            attributeContainer.appendChild(attributeDiv);

            document.getElementById("customAttributeName").value = "";
            document.getElementById("customAttributeValue").value = "";

            var modal = bootstrap.Modal.getInstance(document.getElementById("attributeModal"));
            modal.hide();
        }
    });

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-attribute")) {
            event.target.parentElement.remove();
        }
    });
});