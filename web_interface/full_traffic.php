<!DOCTYPE HTML>
<html>
<title>
Full Traffic
</title>
<head>
<body>
<?php
include("navbar.php");
include_once('connection.php');
$network_id = $_GET['network_id'];
$sql = "SELECT * FROM network_traffic WHERE id = " .$network_id; 
$result = mysqli_query($db, $sql);
$resultCheck = mysqli_num_rows($result);
?>

<?php
if ($resultCheck > 0) {
while($rows=mysqli_fetch_assoc($result)) {
?>

<p style= "padding-left: 2rem; padding-right: 2rem;"> <?php foreach($rows as $key => $value) { echo "<br>";echo "<b>".$key."</b>".": ".$value; echo "<br>"; }?> </p>
<?php
}
}
?>

</body>
</head>
</html>
