function readyFunction( jQuery ) {
    //Load site content
    $.ajax({
        url: "LoadSiteContent.php",
        dataType: "html",
        success: function(Result) {
            $('.container').html(Result);
            // get the actual state from database
            $.ajax({
                url: "CheckActualStateInDatabase.php",
                type: 'POST',
                data: 'JSON',
                success: function(Resolution) {
                    let resList = JSON.parse(Resolution);
                    let index = 1;
                    resList.forEach(element => {
                        if(element == 1){
                            let nid = "#p" + index;
                            $( nid ).prop("checked", true);
                        }
                        index = index + 1;
                    });
                }
            });
            //handle user click -> update database
            $("input").click(function(){
                let id = parseInt($(this).attr('id').replace(/^\D+/g, ''));
                if($(this).prop("checked")){
                    $.ajax({
                        url: "ResTo1.php",
                        type: 'POST',
                        data: {upId:id}
                    });
                }
                else{
                    $.ajax({
                        url: "ResTo0.php",
                        type: 'POST',
                        data: {dwId:id}
                    });
                }
            });

        }
    });

}

$( document ).ready( readyFunction );