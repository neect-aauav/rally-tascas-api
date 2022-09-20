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
        members INT NOT NULL ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    )",
    "CREATE TABLE `rallyneect`.`Members`(
        name VARCHAR(255) NOT NULL ,
        course VARCHAR(255) NOT NULL,
        nmec INT NOT NULL,
        points INT NOT NULL DEFAULT 0 ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    )",
    "CREATE TABLE `rallyneect`.`TeamsMembers`(
        teamID INT NOT NULL ,
        memberID INT NOT NULL ,
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT ,
    	FOREIGN KEY (teamID) REFERENCES Teams(id) ,
    	FOREIGN KEY (memberID) REFERENCES Members(id)
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