<?php
require 'db.php';

$pw = isset($_GET['pw']) ? $_GET['pw'] : null;

if (strlen($pw) > 5) {
	exit ("Password is too long.");
}

$query = "SELECT * FROM users WHERE passwd = '$pw' ";
$result = $pdo->query($query);

if ($result->rowCount() > 0) {
	echo "Login Success";
} else {
	echo "Login Failed";
}
?>

