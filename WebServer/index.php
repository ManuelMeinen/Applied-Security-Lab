<?php
  session_start();

  // If user already logged in, send them to index
  if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true) {
      header('Location:login.php');
      exit;
  }
?>

<!DOCTYPE html>
<html>
    <head>
        <title>iMovie</title>
    </head>
    <body>
        <h2>iMovie</h2>
        <p>Welcome to the iMovie website!</p>
    </body>
</html>