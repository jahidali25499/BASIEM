<?php

include_once("connection.php");

$device_name = $_GET["device_name"];
$device_num = $_GET["device_num"];

$sql = "SELECT * FROM device_configs WHERE device_name = '$device_name'";
$result = mysqli_query($db, $sql);

$check_sql = "SHOW TABLES WHERE Tables_in_BASIEM = '$device_name'";
$check_sql_result = mysqli_query($db, $check_sql);

if (mysqli_num_rows($result) > 0) {

    echo "<script>alert('Hash already generated for this device!')</script>";
    echo "<script>alert('Remove current hash to generate another')</script>";
    echo "<script>window.location.replace('/index.php')</script>";

}

else if (mysqli_num_rows($check_sql_result) == 0) {

	echo "<script>alert('Device configuration not found on database')</script>";
	echo "<script>window.location.replace('/index.php')</script>";
}

else {

	$config_sql = "SELECT properties FROM $device_name WHERE object = 'device:$device_num'";
	$config_result = mysqli_query($db, $config_sql);
	$config_rows = mysqli_num_rows($config_result);

	if ($config_rows > 0) {

		while ($rows=mysqli_fetch_assoc($config_result)){

			$hash = hash("sha256", $rows["properties"]);
			
			if ($insert_sql = mysqli_prepare($db, "INSERT INTO device_configs (device_name, hash) VALUES (?,?)")) {

				mysqli_stmt_bind_param($insert_sql, "ss", $device_name, $hash);
				mysqli_stmt_execute($insert_sql);

				echo "<script>alert('Hash inserted into database')</script>";
				echo "<script>window.location.replace('hashing_page.php')</script>";
			} 

			else {
				echo "<script>alert('Error could not prepare query: ".mysqli_error($db).")</script>";
			}



		}
	}

}



?>
