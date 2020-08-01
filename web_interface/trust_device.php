<?php

include_once("connection.php");

$device_name = $_GET["device_name"];
$device_num = $_GET["device_num"];

$sql = "SELECT * FROM trusted_devices WHERE device_name = '$device_name' AND device_id = $device_num";
$result = mysqli_query($db, $sql);


if (mysqli_num_rows($result) > 0) {

	echo "<script>alert('This Device is Already Trusted!')</script>";
	echo "<script>window.location.replace('/index.php')</script>";

} 

else {

	if ($insert_sql = mysqli_prepare($db, "INSERT INTO trusted_devices (device_name, device_id) VALUES (?,?)")) {

		mysqli_stmt_bind_param($insert_sql, "ss", $device_name, $device_num);
		mysqli_stmt_execute($insert_sql);

		echo "<script>alert('Device Now Trusted!')</script>";
		echo "<script>window.location.replace('trust_device_page.php')</script>";
	}

	else {

		echo "<script>alert('Error could not prepare query: ".mysqli_error($db).")</script>";
	}
}


mysqli_close($db);


?>