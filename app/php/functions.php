<?php

function apiFetch($endpoint) { 
    // Read JSON file
    $json_data = file_get_contents($endpoint);
    
    // Decode JSON data into PHP array
    $response_data = json_decode($json_data, true);
    return $response_data;
}

function makeSQLQuery($conn, $sql, $types, $vars) {
    $stmt = mysqli_stmt_init($conn);
    mysqli_stmt_prepare($stmt, $sql);
    mysqli_stmt_bind_param($stmt, $types, ...$vars);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    return $result;
}