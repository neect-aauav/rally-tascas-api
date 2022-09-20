<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$document_root=$_SERVER['DOCUMENT_ROOT'];

require $document_root.'/php/connect.php';
require $document_root.'/php/functions.php';

// set timezone to Lisbon (Portugal)
date_default_timezone_set("Europe/Lisbon");

$method = $_SERVER['REQUEST_METHOD']; 
if ($method === 'POST') {
    // check if there was a signup submition
    if (isset($_POST['team-submit'])) {
        // fetch information from the signup form
        $team_name = $_POST['team'];
        $team_email = trim($_POST['email']);
        $members_names = $_POST['member'];
        $members_nmecs = $_POST['nmec'];
        $members_courses = $_POST['course'];
        $n_members = count($members_names);
        
        // check if name exists
        $sql = "SELECT * FROM Teams WHERE name=?";
        $stmt = mysqli_stmt_init($conn);
        // check if the query makes sense
        if (!mysqli_stmt_prepare($stmt, $sql)) {
            header("Location: signup.php?submit=error");
            exit();
        }
        else {
            mysqli_stmt_bind_param($stmt, 's', $team_name);
            mysqli_stmt_execute($stmt);
            $result = mysqli_stmt_get_result($stmt);
            if (!mysqli_fetch_assoc($result)) {
                // check if email exists
                $sql = "SELECT * FROM Teams WHERE email=?";
                $stmt = mysqli_stmt_init($conn);
                // check if the query makes sense
                if (!mysqli_stmt_prepare($stmt, $sql)) {
                    header("Location: signup.php?submit=error");
                    exit();
                }
                else {
                    mysqli_stmt_bind_param($stmt, 's', $team_email);
                    mysqli_stmt_execute($stmt);
                    $result = mysqli_stmt_get_result($stmt);
                    if (!mysqli_fetch_assoc($result)) {                
                        // add team
                        $sql = "INSERT INTO Teams (name, email, members) VALUES (?, ?, ?)";
                        $stmt = mysqli_stmt_init($conn);
                        mysqli_stmt_prepare($stmt, $sql);
                        mysqli_stmt_bind_param($stmt, 'ssi', $team_name, $team_email, $n_members);
                        mysqli_stmt_execute($stmt);

                        // add members
                        forEach($members_names as $memberId=>$memberName) {
                            //print_r($memberId);
                            //print_r($members_courses[$memberId]);
                            $sql = "INSERT INTO Members (name, course, nmec) VALUES (?, ?, ?)";
                            $stmt = mysqli_stmt_init($conn);
                            mysqli_stmt_prepare($stmt, $sql);
                            mysqli_stmt_bind_param($stmt, 'ssi', $memberName, $members_courses[$memberId], $members_nmecs[$memberId]);
                            mysqli_stmt_execute($stmt);
                        }
                    }
                    else {
                        // email already exists
                        header("Location: signup.php?submit=email_exists");
                        exit();
                    }
                }
            }
            else {
                // email already exists
                header("Location: signup.php?submit=name_exists");
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
    <title>Signup | Rallyween</title>
</head>
<body>
    <div class="signup-form absolute-centered">
        <p>Equipa</p>
        <form action="signup.php" method="post">
            <div class="team">
                <input placeholder="Nome" type="text" name="team" required>
                <input placeholder="Email" type="email" name="email" required>           
            </div>
            <div class="members">
                <p>Membros</p>
                <div>
                    <input placeholder="Nome" type="text" name="member[0]" required>
                    <input class="nmec-input" placeholder="NMEC" type="text" name="nmec[0]" required>
                    <select name="course[0]" required>
                        <option></option>
                    </select>
                    <div class="remove-member inactive"><div class="absolute-centered"><div></div><div></div></div></div>
                </div>
                <div class="add-member clickable">+ Adicionar Membro</div>
            </div>

            <?php
                if (isset($_GET['submit'])) {
                    switch($_GET['submit']) {
                        case "email_exists":
                            echo "
                                <div style=\"color: red;\">
                                    There is already a team with that email.
                                </div>
                            ";
                            break;
                        case "name_exists":
                            echo "
                                <div style=\"color: red;\">
                                    There is already a team with that name.
                                </div>
                            ";
                            break;
                    }
                }
            ?>

            <input class="clickable" type="submit" value="Criar" name="team-submit">
        </form>
    </div>
    
    <script src="scripts/static.js"></script>
    <script src="scripts/signup.js"></script>
</body>
</html>