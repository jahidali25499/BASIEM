<!DOCTYPE HTML>
<html>
    <head>
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <a class="navbar-brand" >BASIEM</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavDropdown">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="index.php">Devices <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="events.php">Events <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active">  
        <a class="nav-link" href="alerts.php">Alerts <span class="sr-only">(current)</span></a>

      <li class="nav-item active">  
        <a class="nav-link" href="hashing_page.php">Configuration Hashing <span class="sr-only">(current)</span></a>
      <li class="nav-item active">  
        <a class="nav-link" onclick="return confirm('Remove current devices and scan for new ones on network?')" href="refresh_inventory.php">Refresh Inventory <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="index.php">Trusted Devices<span class="sr-only">(current)</span></a>
      </li>
    </div>
    </head>
     <!-- <li class="nav-item">
        <a class="nav-link" href="#">Features</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Pricing</a>
      </li>
    </ul>
  </div>-->
</nav>
</html>
