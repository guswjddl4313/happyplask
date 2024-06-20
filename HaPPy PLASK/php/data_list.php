<?php
    $directory = './uploads/';
    $data_files = array_diff(scandir($directory), array('..', '.', 'index.html'));
    foreach ($data_files as $key => $value) {
        echo "<li><a href='/data?page=data_view&file={$directory}{$value}'>".$value."</a></li><br/>";
    }
?>
