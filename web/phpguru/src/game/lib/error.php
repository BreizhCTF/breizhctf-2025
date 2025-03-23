<?php

$DEBUG = 0;

function errorHandler($errno, $errstr, $errfile, $errline) {    
    echo '<br><br><!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error</title>
        <link rel="stylesheet" href="css/error.css">
        <link rel="icon" href="images/i-love-php.jpg">
    </head>
    <body>
        <div class="error-container">';

    if ($GLOBALS["DEBUG"] == 1) {
        echo "<h1>Yoo dev friend, you'll need this:</h1>";
        echo "<h3>Error Details</h3>";
        echo "<div class='error-details'>";
        echo "<p><strong>Error number:</strong> $errno</p>";
        echo "<p><strong>Error message:</strong> $errstr</p>";
        echo "<p><strong>Error file:</strong> $errfile</p>";
        echo "<p><strong>Error line:</strong> $errline</p>";
        echo "<h3>Backtrace:</h3><pre>";
        print_r(debug_backtrace());
        echo "</pre>";
        echo "<h3>Global Variables at the Time of Error:</h3><pre>";
        print_r($GLOBALS);
        echo "</pre>";
        echo "</div>";
    } else {
        echo "<h1>Something went wrong. Please try again later.</h1>";
    }

    echo '<a href="index.php" class="error-btn">Go Back</a>';
    echo '</div></body></html>';

    exit(1);
}

set_error_handler("errorHandler");
?>
