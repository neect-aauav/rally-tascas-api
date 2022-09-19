<?php

$document_root=$_SERVER['DOCUMENT_ROOT'];

require $document_root.'/php/connect.php';
require $document_root.'/php/functions.php';

// setup tables
$tables = array(
    "CREATE TABLE `rallyneect`.`Teams`(
        name VARCHAR(255) NOT NULL ,
        email VARCHAR(255) NOT NULL ,
        points INT NOT NULL ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    )",
    "CREATE TABLE `rallyneect`.`Members`(
        name VARCHAR(255) NOT NULL ,
        course VARCHAR(255) NOT NULL,
        points INT NOT NULL ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    )",
    "CREATE TABLE `rallyneect`.`teamsMembers`(
        teamId INT NOT NULL FOREIGN KEY Teams(id) ,
        memberId INT NOT NULL FOREIGN KEY Members(id) ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
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