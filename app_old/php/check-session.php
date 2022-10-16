<?php

session_start();

// if not yet in session then go to login
if(!isset($_SESSION["userId"])){
	header("Location: /admin?submit=nologin");
	exit();
}