<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require $_SERVER['DOCUMENT_ROOT'].'/php/connect.php';
require $_SERVER['DOCUMENT_ROOT'].'/php/functions.php';

$method = $_SERVER['REQUEST_METHOD']; 
if ($method === 'GET') {
    header('Content-type: application/json; charset=utf-8');

    $data = Array();

    $sql = "SELECT * FROM Members WHERE 1";
    $result = makeSQLQuery($conn, $sql);
    while($row = mysqli_fetch_assoc($result)) {
        $data[] = $row;
    }

    $response["data"] = $data;
    $response["size"] = count($data);
    date_default_timezone_set("Europe/Lisbon");
    $response["timestamp"] = date('Y-m-d H:i:s');
    echo json_encode($response, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}