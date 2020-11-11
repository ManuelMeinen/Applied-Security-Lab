<?php
  session_start();

  // If user already logged in, send them to index
  if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
      header('Location:index.php?');
      exit;
  }
?>

<html>
    <head>
        <title>login</title>
    </head>
    <body>
        <h2>Login</h2>
        <p>Please login!</p>
    </body>
</html>