<?php


include_once("connection.php");

$device_name = $_GET["device_name"];

$sql = "SELECT hash FROM device_configs WHERE device_name = '$device_name'";
$result = mysqli_query($db, $sql);
$resultCheck = mysqli_num_rows($result);


function find_id($name) {

	include("connection.php");

	$id_sql = "SELECT deviceid FROM inventory_2 WHERE devicename = '$name'";
	$id_result = mysqli_query($db, $id_sql);
	$id_resultCheck = mysqli_num_rows($id_result);

	if ($id_resultCheck > 0) {
		while ($rows = mysqli_fetch_assoc($id_result)) {
			$device_id = $rows["deviceid"];

			return $device_id; 
		}
	}
}


function gen_config_hash($name, $number) {

	include("connection.php");

	$config_sql = "SELECT properties FROM $name WHERE object = 'device:$number'";
	$config_result = mysqli_query($db, $config_sql);
	$config_rows = mysqli_num_rows($config_result);

	if ($config_rows > 0) {

		while ($rows=mysqli_fetch_assoc($config_result)){

			$hash = hash("sha256", $rows["properties"]);
			return $hash;
}
}
}

if ($resultCheck > 0) {

	while ($rows = mysqli_fetch_assoc($result)) {

		$db_hash = $rows["hash"];
		echo "<br>";
		$current_hash = gen_config_hash($device_name, find_id($device_name));

		if ($current_hash === $db_hash) {

			echo "<script>alert('Integrity Check Passed!')</script>";
			echo "<script>window.location.replace('hashing_page.php')</script>";
		}

		else {

			echo "<script>alert('Integrity Checks Failed!')</script>"; 
			echo "<script>window.location.replace('hashing_page.php')</script>";
		}
	}
}


mysqli_close($db);

?>
