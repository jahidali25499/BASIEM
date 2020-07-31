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
$device_name = $_GET['name'];

$sql = "SELECT object, properties FROM " .$device_name;
$result = mysqli_query($db, $sql);
$resultCheck = mysqli_num_rows($result);
?>
<h2 style="text-align:center; margin-top:30px; margin-bottom:30px">Objects</h2>
<body>
<table class="table table-hover" style="width:50%; text-align:center"> 
  <thead class="thead-dark">
    <tr>
      <th scope="col">Object</th>
      <th scope="col" style="width:100%">Properties</th>
    </tr>
  </thead>
  <tbody>
  <?php
if ($resultCheck > 0) {
while($rows=mysqli_fetch_assoc($result))
{
?>
    <tr style="text-align:center">
      <th scope="row"><?php echo $rows['object']; ?></th>
      <th scope="row" style="text-align: left; width:50px"><?php $json_prop = json_decode($rows['properties'], true); foreach($json_prop as $prop => $value) { echo $prop.": ".$value; echo '<br>'; } ?></th>
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
<?php
mysqli_close($db);
?> 
</html>
