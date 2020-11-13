<?php
  session_start();

  // If user already logged in, send them to index
  if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true) {
    header('Location:index.php');
    exit;
  }

  $username = "";
  $password = "";
  $error = "";
  
  // Processing form
  if($_SERVER["REQUEST_METHOD"] == "POST"){
    $username = trim($_POST["username"]);
    $password = trim($_POST["password"]);
  
    if(empty($error)){
      if($username == 'bob' && $password == 'bob') {
        session_start();
                    
        $_SESSION["loggedin"] = true;
        $_SESSION["id"] = $id;
        $_SESSION["username"] = $username;                            
        
        header("location: index.php");
      } else {
        $error = "Invalid credentials.";
      }
    }
  }
?>

<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
</head>
<body>
  <div class="wrapper">
    <h2>Login</h2>
    <p>Please fill in your credentials to login.</p>
    <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
      <div class="form-group">
        <label>Username</label>
        <input type="text" name="username" class="form-control">
      </div>    
      <div class="form-group">
        <label>Password</label>
        <input type="password" name="password" class="form-control">
      </div>
      <div class="form-group">
        <input type="submit" class="btn btn-lg btn-primary" value="Login">
      </div>
      <p><?php echo $error; ?></p>
    </form>
  </div>    
</body>
</html>