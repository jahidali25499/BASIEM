<!DOCTYPE HTML>
<html>
<title>
BASIEM Alerts
</title>
<head>
<?php
include 'navbar.php';
?>
<?php

include_once('connection.php');
$sql = "SELECT * FROM alerts ORDER BY id DESC;";
$result = mysqli_query($db, $sql);
$resultCheck = mysqli_num_rows($result);
?>
<h2 style="text-align:center; margin-top:30px; margin-bottom:30px">Alerts</h2>
<body>
<table id="devices_table" class="table table-hover" style="width:70%; text-align:center"> 
  <thead class="thead-dark">
    <tr>
      <th scope="col">Alert ID</th>
      <th scope="col">Time</th>
      <th scope="col">Alert</th>
      <th scope="col">See Full Traffic</th>
    </tr>
  </thead>
  <tbody>
  <?php
if ($resultCheck > 0) {
while($rows=mysqli_fetch_assoc($result))
{
?>
    <tr style="text-align:left">
      <th style="text-align:center" scope="row"><?php echo $rows['id']; ?></th>   
      <td style="text-align:center"><?php echo $rows['timestamp']; ?></td>
      <td><?php $json_alert=$rows['alert']; $json_array=json_decode($json_alert, true); foreach($json_array as $key=>$value){ echo '<b>'.$key.'</b>'.": ".$value; echo '<br>'; } ?></td>
      <td><a href="<?php $network_id = $rows['id_network_traffic']; echo 'full_traffic.php?network_id='.$network_id; ?>"><img src="icon.png" alt="See Full Traffic" style=height:40px;"></td> 
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
</head>
</html>
