<?php

include "lib/global.php"; 
include "lib/error.php";

if ($_SESSION["gamecompleted"] === false) {
    header("Location: game.php");
    exit();
}

if ($_SESSION["loggedin"] === false) {
    header("Location: login.php");
    exit();
}

if ($_SESSION["gamecompleted"] === true && $_SESSION["loggedin"] === true) {
    header("Location: private.php");
    exit();
}

?>