<?php

$document_root=$_SERVER['DOCUMENT_ROOT'];

require $document_root.'/php/connect.php';
require $document_root.'/php/functions.php';

// setup tables
$tables = array(
    "CREATE TABLE `rallyneect`.`Teams`(
        name VARCHAR(255) NOT NULL ,
        email VARCHAR(255) NOT NULL ,
        points INT NOT NULL DEFAULT 0 ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    )",
    "CREATE TABLE `rallyneect`.`Members`(
        name VARCHAR(255) NOT NULL ,
        course VARCHAR(255) NOT NULL,
        nmec INT NOT NULL,
        points INT NOT NULL DEFAULT 0 ,
        team INT NOT NULL ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        FOREIGN KEY (team) REFERENCES Teams(id)
    )",
    "CREATE TABLE `rallyneect`.`Admin`(
        username VARCHAR(255) NOT NULL ,
        pwd TEXT NOT NULL ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    )",
    "CREATE TABLE `rallyneect`.`Bars`(
        name VARCHAR(255) NOT NULL ,
        location TEXT ,
        picture TEXT ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    )",
    "CREATE TABLE `rallyneect`.`TeamsBars`(
        teamdId INT NOT NULL ,
        barId INT NOT NULL ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT ,
        FOREIGN KEY (teamdId) REFERENCES Teams(id) ,
        FOREIGN KEY (barId) REFERENCES Bars(id)
    )"
);

echo "Adding tables:<br>";
foreach($tables as $table) {
    $table_name = explode("`", $table)[3];
    $result = mysqli_query($conn, "SHOW TABLES LIKE '". $table_name . "';");
    if (mysqli_num_rows($result) == 0) { 
        echo "- Creating table " . $table_name . "<br>";
        mysqli_query($conn, $table);
    }
}

// add admin
$admin_row = mysqli_query($conn, "SELECT * FROM Admin WHERE 1");
if (mysqli_num_rows($admin_row) == 0) { 
    if ($admin_username && $admin_password) {
        $sql = "INSERT INTO Admin (username, pwd) VALUES (?, ?)";
        makeSQLQuery($conn, $sql, 'ss', [$admin_username, password_hash($admin_password, PASSWORD_DEFAULT)]);
        echo "Added Admin";
    }
}