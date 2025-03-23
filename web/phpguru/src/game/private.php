<?php

include "lib/global.php";
include "lib/error.php";
include "lib/security.php";

if (!$_SESSION['gamecompleted'] === true || !$_SESSION['loggedin'] === true) {
    header('Location: index.php');
    exit();
}

header('Game-Number: 03');

$poems_dir = "poems/";
$available_poems = [];

if (is_dir($poems_dir)) {
    $files = scandir($poems_dir);
    foreach ($files as $file) {
        if ($file !== "." && $file !== ".." && $file !== "invalid.txt" && pathinfo($file, PATHINFO_EXTENSION) === "txt") {
            $available_poems[] = pathinfo($file, PATHINFO_FILENAME);
        }
    }
}

$message = "";
$poem_content = "";
$poem_name = "";

if (isset($_GET['poem'])) {
    $poem = $_GET['poem'];
    if (preg_match('/^[a-z0-9-]+$/', $poem)) {
        $poem_name = $poems_dir . $poem . ".txt";
    } else {
        $poem_name = sanitize($poem);
    }

    try {
        $handle = fopen($poem_name, "r");
        if ($handle) {
            while (($line = fgets($handle)) !== false) {
                $poem_content .= $line;
            }
            fclose($handle);
        } else {
            $message = "⚠️ Erreur lors de l'ouverture du poème.";
        }
    } catch (Exception $e) {
        $message = "⚠️ Erreur lors de l'ouverture du poème.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Guru - Bibliothèque</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/private.css">
    <script src="js/bootstrap.min.js" defer></script>
    <link rel="icon" href="images/i-love-php.jpg">
</head>
<body>

<div class="container d-flex flex-column justify-content-center align-items-center vh-100">
    <div class="card shadow-lg p-4 text-center animate__animated animate__fadeIn">
        <h1 class="mb-3 text-primary">Bibliothèque à Poèmes</h1>
        <p class="fs-5">Quel poème souhaitez-vous lire ?</p>

        <?php if ($message): ?>
            <div class="alert alert-danger fade show animate__animated animate__fadeIn" role="alert">
                <?= $message; ?>
            </div>
        <?php endif; ?>

        <div class="list-group mt-3">
            <?php foreach ($available_poems as $poem): ?>
                <a href="?poem=<?= htmlspecialchars($poem); ?>" class="list-group-item list-group-item-action stylish-list">
                    📖 <?= ucfirst(str_replace("-", " ", $poem)); ?>
                </a>
            <?php endforeach; ?>
        </div>

        <?php if ($poem_content): ?>
            <div class="mt-4 p-3 bg-light border rounded shadow animate__animated animate__fadeIn">
                <h3 class="text-secondary"><?= ucfirst(str_replace("-", " ", basename($poem_name, ".txt"))); ?></h3>
                <pre class="text-start"><?= htmlspecialchars($poem_content); ?></pre>
            </div>
        <?php endif; ?>
    </div>
</div>

</body>
</html>
