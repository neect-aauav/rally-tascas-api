<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$document_root=$_SERVER['DOCUMENT_ROOT'];

require $document_root.'/php/connect.php';
require $document_root.'/php/functions.php';

session_start();

// set timezone to Lisbon (Portugal)
date_default_timezone_set("Europe/Lisbon");

// destroy session if logout
if (isset($_GET['submit']) && $_GET['submit'] == "logout")
    session_destroy();
// if already in session then go to home
else if(isset($_SESSION["userId"])){
    header("Location: admin/bars");
    exit();
}

$method = $_SERVER['REQUEST_METHOD']; 
if ($method === 'POST') {
    // check if there was a login submition
    if (isset($_POST['login-submit'])) {
        // fetch information from the login form
        $username = trim($_POST['username']);
        $pwd = $_POST['password'];

        // check if username exists
        $sql = "SELECT * FROM Admin WHERE username=?;";
        $stmt = mysqli_stmt_init($conn);
        // check if the query makes sense
        if (!mysqli_stmt_prepare($stmt, $sql)) {
            header("Location: admin?submit=error");
            exit();
        }
        else {
            // use binding to prevent executing queries from the user
            mysqli_stmt_bind_param($stmt, 's', $username);
            mysqli_stmt_execute($stmt);
            $result = mysqli_stmt_get_result($stmt);
            // fetch rows
            if ($row = mysqli_fetch_assoc($result)) {
                $pwd_check = password_verify($pwd, $row['pwd']);
                if ($pwd_check == true){
                    session_start();

                    $_SESSION['userId'] = $row["id"];

                    header("Location: admin?submit=login");
                    exit();
                }
                else {
                    // Password is incorrect
                    header("Location: admin?submit=invalid");
                    exit();
                }
            }
            else {
                // Username not found
                header("Location: admin?submit=invalid");
                exit();
            }
        }
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/signup.css">
    <title>Login | Rallyween</title>
</head>
<body>
    <div class="form absolute-centered">
        <p>Admin</p>
        <form action="admin.php" method="post">
            <div class="admin">
                <input placeholder="Username" type="text" name="username" required>
                <input placeholder="Password" type="password" name="password" required>           
            </div>

            <?php
                if (isset($_GET['submit'])) {
                    switch($_GET['submit']) {
                        case "nologin":
                            echo "
                                <div style=\"color: red;\">
                                    Precisas de estar autenticado.
                                </div>
                            ";
                            break;
                        case "invalid":
                            echo "
                                <div style=\"color: red;\">
                                    Username ou passwords errados.
                                </div>
                            ";
                            break;
                        case "login":
                            echo "
                                <div style=\"color: green;\">
                                    Sessão iniciada.
                                </div>
                            ";
                            break;
                    }
                }
            ?>

            <input class="clickable" type="submit" value="Login" name="login-submit">
        </form>
    </div>
    
    <script src="scripts/static.js"></script>
    <script src="scripts/login.js"></script>
</body>
</html>