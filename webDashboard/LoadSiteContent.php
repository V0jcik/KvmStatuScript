<?php
    require 'nothingImportant.php'; // import sensitive data

    $mysqli = mysqli_connect($host,$user,$password,$database); // connection to database [SELECT ONLY]

    if ($mysqli->connect_error) {
        die("Connection failed: " . $mysqli->connect_error);
    }
    $qst = $mysqli->query('SELECT * FROM info;');  // SELECT all data from TABLE
    
    while($row = $qst->fetch_row()){  // fetch selected data

        echo "<div class='kvmcard ".(($row[2] != 0) ? 'cardstateup' : 'cardstatedown')."'>";
        
        // RESERVED pill
        echo "<div id='checkbox-".$row[0]."' class='check-box'>
                <div class='item'>
                    <div class='toggle-pill-color".(($row[2]==0) ? ' disable' : '')."'>
                        <input type='checkbox' id='p".$row[0]."' name='".$row[1]."'>              
                        <label for='p".$row[0]."'></label>
                    </div>
                </div>
            </div>";

        echo "
                <div class='icon'></div>
                    <div class='kvminfo'>
                        <div class='title'>KVM ".$row[0]."</div>

                        <div class='state ".(($row[2] != 0) ? 'stateup' : 'statedown')."'>State: </div>";
                        // ($row[4] != NULL) ? "<div class='uptime'></div>" : ''
                        if($row[3] != NULL){
                            echo "
                                <a href='".sprintf('https://console%s.kvm.example.com', $row[0])."'>Console&#128272;(SSL)</a>
                                <a href='".sprintf('http://console%s.kvm.example.com', $row[0])."'>Console&#x1F513;</a>
                            ";
                        }

                        // Timer since console activation

                        if($row[3] != 0 && $row[3] != NULL){
                            $secInterval = strtotime(date('y-m-d H:i:s')) - strtotime(date($row[3]));
                            $hours = round($secInterval / 60 / 60 , 1);

                            if($hours >= 24){
                                $days = intval($hours / 24);
                                $hour = $hours - $days * 24;
                                echo "<div class='uptime'>Uptime: ".$days."d, ".$hour."h</div>";
                            }
                            else{
                                echo "<div class='uptime'>Uptime: ".$hours."h</div>";
                            }                                          
                        }
        echo
                "</div>
            </div>";
    }

    $mysqli->close();
?>