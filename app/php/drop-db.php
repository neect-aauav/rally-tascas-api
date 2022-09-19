<?php

$method = $_SERVER['REQUEST_METHOD']; 
if ($method === 'GET') {
    if (isset($_GET["db_host"]) && isset($_GET["db_username"]) && isset($_GET["db_password"]) && isset($_GET["db_name"])) {
        if ($_GET["db_password"] == "''") $_GET["db_password"] = "";
        echo $_GET["db_password"];
        $conn = mysqli_connect($_GET["db_host"], $_GET["db_username"], $_GET["db_password"], $_GET["db_name"]);
        if ($conn) {
            $query = "DROP DATABASE ". $_GET["db_name"];
            $result = mysqli_query($conn, $query);
            echo "Database '". $_GET["db_name"] ."' dropped.";
        }
    }
}