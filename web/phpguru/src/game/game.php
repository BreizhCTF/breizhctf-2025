<?php

include "lib/global.php";
include "lib/error.php";

if ($_SESSION["loggedin"] === false) {
    header("Location: login.php");
    exit();
}

if ($_SESSION["gamecompleted"] === true) {
    header("Location: game.php");
    exit();
}

$date = new DateTime();
$today_date = $date->format('d-m-Y');
$real_year = (int) date("Y");
$real_year_last_digit = $real_year % 10;
$message = "";
$alert_type = "";

if (isset($_GET["year"])) {
    $year = $_GET["year"];
    $year_int = (int) $year;

    if (str_contains($year, (string) $real_year_last_digit)) {
        $message = "L'année ne peut contenir le chiffre " . $real_year_last_digit . ".";
        $alert_type = "danger";
    } elseif (!is_numeric($year)) {
        $message = "Une année devrait être un nombre, un peu d'effort...";
        $alert_type = "warning";
    } elseif ($year_int === $real_year) {
        $_SESSION["gamecompleted"] = true;
        $message = "🎉 Bravo ! Vous pouvez accéder à l'étape suivante <a href='index.php'>ici</a>.";
        $alert_type = "success";
    } else {
        $message = "❌ Non, ce n'est pas ça. Réessayez !";
        $alert_type = "danger";
    }
}

header('Game-Number: 2/3');
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHPGuru - Année Devinette</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/main.css">
    <script src="js/bootstrap.min.js" defer></script>
    <link rel="icon" href="images/i-love-php.jpg">
</head>
<body>

<div class="container d-flex flex-column justify-content-center align-items-center vh-100">
    <div class="card shadow-lg p-4 text-center animate__animated animate__fadeIn">
        <h1 class="mb-3 text-primary">Oh, encore vous !</h1>
        <p class="lead">Aujourd'hui, nous sommes le <strong><?= $today_date; ?></strong></p>
        <p class="fs-5">En quelle année sommes nous ?</p>

        <?php if ($message): ?>
            <div class="alert alert-<?= $alert_type; ?> fade show animate__animated animate__fadeIn" role="alert">
                <?= $message; ?>
            </div>
        <?php endif; ?>

        <form action="" method="GET" class="mt-3">
            <div>
                <input type="text" name="year" class="form-control stylish-input" placeholder="Entrez l'année" required>
                <button type="submit" class="btn btn-primary stylish-button mt-2">Envoyer</button>
            </div>
        </form>
    </div>
</div>

</body>
</html>
