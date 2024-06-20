<html>
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
<title>Data Center</title>
</head>
<body>
    <div id="navbar">
        <ul class="nav navbar-nav">
            <li><a href="/data?page=data_list">List</a></li>
            <li><a href="/admin">Admin</a></li>
        </ul>
    </div>
    <div class="container">
      <?php
          $allowed_pages = ['data_list', 'data_readme', 'data_view'];
          $page = isset($_GET['page']) ? $_GET['page'] : 'data_readme';

		  if (in_array($page, $allowed_pages)) {
              include $page . '.php';
		  } else {
              $content = file_get_contents($page . '.php');
              echo $content;
		  }
      ?>
    </div>
</body>
</html>

