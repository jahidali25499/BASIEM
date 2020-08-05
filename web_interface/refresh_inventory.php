<?php


exec("python3 refresh_inventory.py");

echo "<script>alert('Inventory refresh completed')</script>";
echo "<script>window.location.replace('/index.php')</script>";

?>
