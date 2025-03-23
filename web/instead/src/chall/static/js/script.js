var isLogin = true;

const clearErrorBox = () => {
    let errorBox = document.getElementById("errorBox");
    errorBox.style.display = "none";
    errorBox.innerHTML = "";
};

const clearSuccessBox = () => {
    let successBox = document.getElementById("successBox");
    successBox.style.display = "none";
    successBox.innerHTML = "";
};

const displayError = (message) => {
    let errorBox = document.getElementById("errorBox");
    errorBox.style.display = "block";
    errorBox.innerHTML = `${message}`;
};

const displaySuccess = (message) => {
    let successBox = document.getElementById("successBox");
    successBox.style.display = "block";
    successBox.innerHTML = `${message}`;
};

const switchAuthMode = () => {
    isLogin = !isLogin;

    document.getElementById("toggleText").innerHTML = isLogin
        ? "Prêt à passer à l'étape suivante ?"
        : "Créez un compte pour continuer";

    document.getElementById("submitButton").innerText = isLogin ? "Continuer →" : "S'inscrire →";
    document.getElementById("submitButton").onclick = isLogin ? () => login() : () => register();

    document.getElementById("switchModeText").innerHTML = isLogin
        ? 'Pas encore inscrit ? <a role="button" class="link-underline-primary" onclick="switchAuthMode()">Créer un compte</a>'
        : 'Déjà inscrit ? <a role="button" class="link-underline-primary" onclick="switchAuthMode()">Se connecter</a>';
};

const sendAuthRequest = async (endpoint, username, password) => {
    return await fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });
};

const login = async () => {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    clearErrorBox();
    try {
        let response = await sendAuthRequest("/login", username, password);
        let data = await response.json();
        if (response.status === 200) {
            window.location.replace("/home");
        } else {
            displayError(data.message);
        }
    }
    catch(e) {
        displayError("Une erreur interne s'est produite");
    }
}

const register = async () => {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    clearErrorBox();
    clearSuccessBox();
    try {
        let response = await sendAuthRequest("/register", username, password);
        let data = await response.json();
        if (response.status === 201) {
            switchAuthMode();
            displaySuccess(data.message);
        } else {
            displayError(data.message);
        }
    }
    catch(e) {
        displayError("Une erreur interne s'est produite");
    }
}

const toggleCommentSection = (postId) => {
    const commentSection = document.getElementById(`comment-section-${postId}`);
    commentSection.style.display = commentSection.style.display === "block" ? "none" : "block";
}