<pre>
<?php
    $file = $_GET['file']?$_GET['file']:'data_readme.php';
    if(preg_match('/key|:/i', $file)){
        exit('You can\'t access this file');
    }
    echo file_get_contents($file);
?>
</pre>
