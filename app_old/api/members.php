<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require $_SERVER['DOCUMENT_ROOT'].'/php/connect.php';
require $_SERVER['DOCUMENT_ROOT'].'/php/functions.php';

$PROTOCOL = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] == 'on' ? "HTTPS" : "HTTP";

$method = $_SERVER['REQUEST_METHOD']; 
if ($method === 'GET') {
    header('Content-type: application/json; charset=utf-8');

    $response = array();
    $data = array();
    $filter = 1;
    $columns = "*";

    if (isset($_GET["id"])) $filter = "id = '".$_GET["id"]."'";
    else if (isset($_GET["name"])) $filter = "name LIKE '%". $_GET["name"] ."%'";
    else if (isset($_GET["course"])) $filter = "course LIKE '%". $_GET["course"] ."%'";
    else if (isset($_GET["nmec"])) $filter = "nmec LIKE '%". $_GET["nmec"] ."%'";

    $sql = "SELECT ". $columns ."  FROM Members WHERE ". $filter;
    $result = makeSQLQuery($conn, $sql);
    while($row = mysqli_fetch_assoc($result)) {
        $row["team"] = apiFetch($PROTOCOL . "://" . $_SERVER['SERVER_NAME'] . "/api/teams?id=" . $row['team']);
        $data[] = $row;
    }

    $response["data"] = $data;
    $response["size"] = count($data);
    date_default_timezone_set("Europe/Lisbon");
    $response["timestamp"] = date('Y-m-d H:i:s');
    echo json_encode($response, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}