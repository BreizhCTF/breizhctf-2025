<?php

include "lib/global.php";
include "lib/error.php";

if ($_SESSION["loggedin"] === true){
    header("Location: private.php");
    exit();
}

if (!getenv("PASSWORD")) {
    die('<div class="container text-center mt-5"><div class="alert alert-danger">Password not set, please set the <strong>PASSWORD</strong> environment variable.</div></div>');
}

extract($_GET);

$PASSWORD = getenv("PASSWORD");
$message = "";
$alert_type = "";

if (isset($password)) {
    if ($password === $PASSWORD) {
        $_SESSION["loggedin"] = true;
        $message = "🎉 Bien joué ! Vous pouvez accéder à l'étape suivante <a href='index.php'>ici</a>.";
        $alert_type = "success";
    } else {
        $message = "❌ Mauvais mot de passe. Réessayez !";
        $alert_type = "danger";
    }
}

header('Game-Number: 1/3');
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Guru - Mot de Passe</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/main.css">
    <script src="js/bootstrap.min.js" defer></script>
    <link rel="icon" href="images/i-love-php.jpg">
</head>
<body>

<div class="container d-flex flex-column justify-content-center align-items-center vh-100">
    <div class="card shadow-lg p-4 text-center animate__animated animate__fadeIn">
        <h1 class="mb-3 text-primary">Bienvenue !</h1>
        <p class="fs-5">Quel est le mot de passe ?</p>

        <?php if ($message): ?>
            <div class="alert alert-<?= $alert_type; ?> fade show animate__animated animate__fadeIn" role="alert">
                <?= $message; ?>
            </div>
        <?php endif; ?>

        <form action="" method="GET" class="mt-3">
            <div>
                <input type="password" name="password" class="form-control stylish-input" placeholder="Entrez le mot de passe" required>
                <button type="submit" class="btn btn-primary stylish-button mt-2">Envoyer</button>
            </div>
        </form>
    </div>
</div>

</body>
</html>
