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
        $("#drop_twitter").click(twitter_top_hastags);
        $("#drop_instagram").click(instagram_top_hastags);
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
        var tweetit = $(".tweet");
        var data = tweetit[0].getAttribute("tweetID")
        $.ajax({
            method: "POST",
            url: '/fetchTweets',
            contentType: 'application/json',
            data: JSON.stringify(String(data)),
            dataType: "json",
            success: function(data) {
                alert(data['result'].length);
                if (JSON.stringify(data['result'].length) > 0) {
                    for (var i = 0; i < JSON.stringify(data['result'].length); i++) {
                        var testi = '<div class="tweet" tweetID="'+
                        String(data.result[i])+'"></div>';
                        $(testi).insertAfter( "h2" );
                        $("#div_twitter div").slice(-1).remove();
                    };
                    twitteriStriimi2(data['result']);
                    console.log(data['result']);
                    console.log(data['result'][0]);
                }
            }
        });
    }

    function fetchInstas() {
        $.ajax({
            
        })
    }

    function twitteriStriimi2(lista) {
        var tweets = document.getElementsByClassName("tweet");
        for (i = 0; i < lista.length; i++) {
            var id = tweets[i].getAttribute("tweetID");
            twttr.widgets.createTweet(lista[i], tweets[i],{
                conversation : 'none',    // or all
                cards        : 'visible',  // or visible 
                linkColor    : '#cc0000', // default is blue
                theme        : 'light'    // or dark
            });
        }; 
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


    function twitter_top_hastags(e) {
        e.preventDefault();
        $.post('/hashtags',
            function(data) {
                $("#twitter_top1").text(data.result[1]);
                $("#twitter_top2").text(data.result[2]);
                $("#twitter_top3").text(data.result[3]);
                $("#twitter_top4").text(data.result[4]);
                $("#twitter_top5").text(data.result[5]);
            })
        //$.ajax({
        //    dataType: "json",
        //    url: "{{ url_for(filename='hashtags_twitter.py') }}",
        //    success: function(data) {
         //       alert("data[0]");
        //    }
        //});
    }


    function instagram_top_hastags(e) {
        e.preventDefault();
        $.post('/hashtags_insta',
            function(data) {
                $("#instagram_top1").text(data.result[1]);
                $("#instagram_top2").text(data.result[2]);
                $("#instagram_top3").text(data.result[3]);
                $("#instagram_top4").text(data.result[4]);
                $("#instagram_top5").text(data.result[5]);
            })
        //$.ajax({
        //    dataType: "json",
        //    url: "{{ url_for(filename='hashtags_twitter.py') }}",
        //    success: function(data) {
         //       alert("data[0]");
        //    }
        //});
    }


    function haeTagilla(tagi) {
        send = {"tagi" : tagi};
        $.ajax({
            dataType: "json",
            method: "POST",
            url: "/hae_twitter_tagilla",
            contentType: "application/json;charset=UTF-8",
            data: JSON.stringify({"tagi" : tagi}),
            //data: JSON.stringify(String(tagi)),
            success: function(data) {
                //alert(data.result);
            }
        });

    }


