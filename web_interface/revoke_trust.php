<?php

include_once("connection.php");

$device_name = $_GET["device_name"];
$device_num = $_GET["device_num"];

$sql = "DELETE FROM trusted_devices WHERE device_name = '$device_name' AND device_id = '$device_num'";

if (mysqli_query($db, $sql)) {

	echo "<script>alert('Device trust has been revoked')</script>";
	echo "<script>window.location.replace('/trust_device_page.php')</script>";
}

else {

	echo "Error deleting records: ".mysqli_error($db);
}

mysqli_close($db);

?>



