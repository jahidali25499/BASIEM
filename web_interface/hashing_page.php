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
$sql = "SELECT * FROM device_configs;";
$result = mysqli_query($db, $sql);
$resultCheck = mysqli_num_rows($result);
?>
<h2 style="text-align:center; margin-top:30px; margin-bottom:30px">Current Device Configuration Hashes</h2>
<body>
<table id="devices_table" class="table table-hover" style="width:70%; text-align:center"> 
  <thead class="thead-dark">
    <tr>
      <th scope="col">Device Name</th>
      <th scope="col">Created On</th>
      <th scope="col">SHA256 Hash</th> 
      <!-- <th scope="col">Events</th> -->
      <th scope="col"></th>
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
      <th scope="row"><?php echo htmlspecialchars($rows['device_name']); ?></th>   
      <td><?php echo $rows['time_stamp']; ?></td>
      <td><?php echo $rows['hash']; ?></td>
      <!-- <td><a href="events.php"><img src="icon.png" alt="Events" style="height:30px;"></td> -->
      <td><button type="button" class="btn btn-dark"><a href="<?php $device_name=htmlspecialchars($rows['device_name']); echo 'integrity.php?device_name='.$device_name; ?>" style="color: white" onclick="return confirm('Check Integrity?')">Check Integrity</a></button></td>
      <td><button type="button" class="btn btn-dark"><a href="<?php $device_name=htmlspecialchars($rows['device_name']); echo 'delete_hash.php?device_name='.$device_name; ?>" style="color: white" onclick="return confirm('Delete this hash?')">Delete Hash</a></button></td>
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
