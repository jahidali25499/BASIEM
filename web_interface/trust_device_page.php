<!DOCTYPE HTML>
<html>
<title>
BASIEM WebApp
</title>
<head>
<?php
include 'navbar.php';
?>
<?php
include_once('connection.php');
$sql = "SELECT * FROM trusted_devices;";
$result = mysqli_query($db, $sql);
$resultCheck = mysqli_num_rows($result);
?>
<h2 style="text-align:center; margin-top:30px; margin-bottom:30px">Current Trusted Devices</h2>
<body>
<table id="devices_table" class="table table-hover" style="width:70%; text-align:center"> 
  <thead class="thead-dark">
    <tr>
      <th scope="col">Device Name</th>
      <th scope="col">Device ID</th>
      <!-- <th scope="col">Events</th> -->
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
  <?php
if ($resultCheck > 0) {
while($rows=mysqli_fetch_assoc($result))
{
?>
    <tr style="text-align:center">
      <th scope="row"> <?php echo htmlspecialchars($rows['device_name']); ?></th>   
      <td><?php echo $rows['device_id']; ?></td>
      <!-- <td><a href="events.php"><img src="icon.png" alt="Events" style="height:30px;"></td> -->
      <td><button type="button" class="btn btn-dark"><a href="<?php $device_name=htmlspecialchars($rows['device_name']); $device_num=$rows['device_id']; echo 'revoke_trust.php?device_name='.$device_name.'&device_num='.$device_num; ?>" style="color: white" onclick="return confirm('Remove device from being trusted?')">Revoke Trust</a></button></td>
   
	  </tr>
  </tbody>

<?php 
}
}

?>
</table>
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</body>
<?php
mysqli_close($db);
?> 
</head>
</html>
