<html>
<body>
<?php
include_once('connection.php');
$query = "SELECT * FROM inventory ;";

 
 
echo '<table border="0" cellspacing="2" cellpadding="2"> 
      <tr> 
          <td> <font face="Arial">device id</font> </td> 
          <td> <font face="Arial">dsa</font> </td> 
          <td> <font face="Arial">Value3</font> </td> 
          <td> <font face="Arial">das</font> </td> 
      </tr>';
 
if ($result = $mysqli->query($query)) {
    while ($row = $result->fetch_assoc()) {
        $id = $row["id"];
        $lastseen = $row["lastseen"];
        $object = $row["object"];
        $properties = $row["properties"];
 
        echo '<tr> 
                  <td>'.$id.'</td> 
                  <td>'.$lastseen.'</td> 
                  <td>'.$object.'</td> 
                  <td>'.$properties.'</td> 
              </tr>';
    }
    $result->free();
} 
?>
</body>
</html>