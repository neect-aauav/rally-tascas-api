<?php

session_start();

// if not yet in session then go to login
if(!isset($_SESSION["userId"])){
	header("Location: /login?submit=nologin");
	exit();
}