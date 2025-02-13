<?php
    //UPDATE res [Reservation] to 1

    $id = $_POST['upId'];

    require 'nothingImportant.php'; // import sensitive data

    $mysqli = mysqli_connect($host,$ajaxUser,$ajaxPassword,$database); // connection to database [SELECT, UPDATE (res)]

    if ($mysqli->connect_error) {
        die("Connection failed: " . $mysqli->connect_error);
    }

    $mysqli->query(sprintf('UPDATE info SET res = 1 WHERE id = %s;', $id)); // UPDATE res value
                    // echo sprintf('UPDATE info SET res = 1 WHERE id = %s;', $id);
    $mysqli->close();
?>