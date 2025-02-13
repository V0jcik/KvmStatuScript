<?php
    require 'nothingImportant.php'; // import sensitive data

    $mysqli = mysqli_connect($host,$user,$password,$database); // connection to database [SELECT ONLY]

    if ($mysqli->connect_error) {
        die("Connection failed: " . $mysqli->connect_error);
    }
    $qst = $mysqli->query('SELECT res FROM info;');  // SELECT res values from TABLE info
    
    $resList = array();

    while($row = $qst->fetch_row()){  // fetch selected data
        array_push($resList, intval($row[0]));
    }
    
    echo json_encode($resList);

    $mysqli->close();

?>