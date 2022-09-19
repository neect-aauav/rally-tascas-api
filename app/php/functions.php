<?php

function apiFetch($endpoint) { 
    // Read JSON file
    $json_data = file_get_contents($endpoint);
    
    // Decode JSON data into PHP array
    $response_data = json_decode($json_data, true);
    return $response_data;
}