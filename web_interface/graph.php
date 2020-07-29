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

$sql = "SELECT devicename, time_stamp, present_value FROM Properties WHERE objectname='analogInput:1';";
$result = mysqli_query($db, $sql);
$resultCheck = mysqli_num_rows($result);
?>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['TimeStamp', 'Value'],
          <?php
          if(mysqli_num_rows($result) > 0){
            while($rows =mysqli_fetch_array($result)){
              echo "['" .$rows['time_stamp']."', ".$rows['present_value']."],";
            }
          }
          ?>
        ]);

        var options = {
          title: 'Bacnet Device',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
</head>
<h2 style="text-align:center; margin-top:30px; margin-bottom:30px">Objects</h2>
<body>
<div id="curve_chart" style="width: 900px; height: 500px"></div>
<table class="table table-hover" style="width:50%; text-align:center"> 
  <thead class="thead-dark">
    <tr>
      <th scope="col">Device</th>
      <th scope="col">TimeStamp</th>
      <th scope="col">PresentValue</th>
    </tr>
  </thead>
  <tbody>
<?php
if ($resultCheck > 0) {
while($rows=mysqli_fetch_assoc($result))
{
?>
    <tr style="text-align:center">
      <th scope="row"><?php echo $rows['devicename']; ?></th>
      <th scope="row"><?php echo $rows['time_stamp']; ?></th>
      <th scope="row"><?php echo $rows['present_value']; ?></th>
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
