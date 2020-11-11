<?php
    if (!isset($_SESSION["userid"]) || $_SESSION["userid"] !== true) {
        header("location:login.php");
        exit;
    }
?>

<html>
    <head>
        <title>iMovie</title>
    </head>
    <body>
        <h2>iMovie</h2>
        <p>Welcome to the iMovie website!</p>
    </body>
</html>