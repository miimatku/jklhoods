    // Javascript source code
    window.onload = function(){
    	alustus();
    	twitteriStriimi();
        instagramBlock();
    }

    function alustus() {
        $("#show_twitter").click(show_twitter);
        $("#show_insta").click(show_instagram);
        $("#show_all").click(show_all);
    }

    function instagramBlock() {
    //    http://api.instagram.com/oembed?url=http://instagr.am/p/{shortcode}
    // theUrl, callback
        var Url = "//api.instagram.com/oembed?url=http://instagr.am/p/"
        var instaposts = $(".instapost");
        instaposts.each(function(index){
            var shortcode = this.getAttribute("instacode");
            var theUrl = Url.concat(shortcode);
            var paikka = this;
            $.ajax({
                type: "GET",
                dataType: "jsonp",
    //        cache: false,
                url: theUrl,
                success: function(response) {
//                    $("instacode='"+shortcode+"'").html(response['html']);
                    $(paikka).html($.parseHTML(response['html']));
                    instgrm.Embeds.process();
                }
            });

        });
        //instgrm.Embeds.process();

    /*    var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                callback(xmlHttp.responseText);
        }
        xmlHttp.open("GET", theUrl, true); // true for asynchronous 
        xmlHttp.send(null);
    */
    }

    function fetchTweets() {
        $.ajax({
            
        })
    }

    function fetchInstas() {
        $.ajax({
            
        })
    }


    function twitteriStriimi() {
    	 var tweets = document.getElementsByClassName("tweet");
        for (i = 0; i < tweets.length; i++) {
            var id = tweets[i].getAttribute("tweetID");
            twttr.widgets.createTweet(id, tweets[i],{
                conversation : 'none',    // or all
                cards        : 'visible',  // or visible 
                linkColor    : '#cc0000', // default is blue
                theme        : 'light'    // or dark
            });
        }; 
    }


    //Show all feed
    function show_all(e){
        e.preventDefault();
        $("#div_twitter").show();
        $("#div_insta").show();
        $("#div_insta").addClass("col-md-6");
        $("#div_twitter").addClass("col-md-6");
    }


    //Show only twitter feed
    function show_twitter(e){
    	e.preventDefault();
    	$("#div_insta").hide();
        $("#div_twitter").show();
    	$("#div_twitter").removeClass("col-md-6");
    }


    //Show only instagram feed
    function show_instagram(e){
        e.preventDefault();
        $("#div_twitter").hide();
        $("#div_insta").show();
        $("#div_insta").removeClass("col-md-6")
    }

