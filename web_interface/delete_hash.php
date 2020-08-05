<?php


include_once("connection.php");

$device_name = $_GET["device_name"];

$delete_sql = "DELETE FROM device_configs WHERE device_name = '$device_name'";

if (mysqli_query($db, $delete_sql)) {

	echo "<script>alert('Hash deleted from database')</script>";
	echo "<script>window.location.replace('hashing_page.php')</script>";
}

else {

	echo "<script>alert('Error deleting record: '.$mysqli_error($db).'</script>'";
}

mysqli_close($db);

?>
