const bt = document.getElementById("open-picker");
const picker = document.getElementById("picker");

const open = e => {
    picker.setAttribute('open', true);
};
const update = e => {
    console.log(e.detail.hex);
    var input = document.getElementById("new-colour");
    input.value = e.detail.hex;
};
bt.addEventListener('click', open);
picker.addEventListener('update-color', update);