    // Javascript source code
    window.onload = function(){
    	alustus();
    	twitteriStriimi(10);
        instagramBlock();
//        fetchTweets();
        ajastin = setInterval(fetchTweets.bind(null, false), 5000);
    }

    function alustus() {
        $("#show_twitter").click(show_twitter);
        $("#show_insta").click(show_instagram);
        $("#show_all").click(show_all);
        $("#drop_twitter").click(twitter_top_hastags);
        $("#drop_instagram").click(instagram_top_hastags);
        $("#uusia_twiitteja").click(function() {
//            e.preventDefault();
            $(this).hide();
            fetchTweets(true);
        });
        $("#hae_seuraavat").click( function(){ haeSeuraavat(); } );
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

    function fetchTweets(jatka) {
        var tweetit = $(".tweet");
        var data = tweetit[0].getAttribute("tweetID");
        $.ajax({
            method: "POST",
            url: '/fetchTweets',
            contentType: 'application/json',
            data: JSON.stringify(String(data)),
            dataType: "json",
            success: function(data) {
                var count = data['result'].length;
                if (count > 0) {
                    if (jatka === true) {
                        for (var i = 0; i < count; i++) {
                            var testi = '<div class="tweet" tweetID="'+
                            String(data.result[i])+'"></div>';
                            $(testi).insertAfter( "#uusia_twiitteja" );
                            $("#div_twitter div").slice(-1).remove();
          //  data.result[i].
                        };
                        twitteriStriimi(count);
                    } else {
                        $('#uusia_twiitteja').show();
                    };
                };
            }
        });
    }

    function uusiaTwiitteja(count, elements) {
        
        for (var i = 0; i < count; i++) {
            var testi = '<div class="tweet" tweetID="'+
            String(data.result[i])+'"></div>';
            $(testi).insertAfter( "h2" );
            $("#div_twitter div").slice(-1).remove();
          //  data.result[i].
        };
        twitteriStriimi(count);
    }

    function haeSeuraavat() {
        var data = $(".tweet:last")[0].getAttribute("tweetid");
        $.ajax({
            method: "POST",
            url: '/haeSeuraavat',
            contentType: 'application/json',
            data: JSON.stringify(String(data)),
            dataType: "json",
            success: function(data) {
                var count = data['result'].length;
                        for (var i = 0; i < count; i++) {
                            var testi = '<div class="tweet" tweetID="'+
                            String(data.result[i])+'"></div>';
                            $(testi).insertBefore( "#hae_seuraavat" );
          //  data.result[i].
                        };
                        twitteriStriimi(-1);
            }
        });
    }

    function twitteriStriimi(count) {
        var tweets;
        if (count > 10) {
            tweets = d$(".tweet").slice(0,10);
            new_tweets = 10;
        } else if (count === -1) {
            tweets = $('.tweet').slice(-10);
            new_tweets = 10;
        } else {
            tweets = $(".tweet").slice(0,count);
            new_tweets = count;
        }
        for (i = 0; i < new_tweets; i++) {
            var id = tweets[i].getAttribute("tweetID");
            twttr.widgets.createTweet(id, tweets[i],{
                conversation : 'none',    // or all
                cards        : 'visible',  // or visible 
                linkColor    : '#cc0000', // default is blue
                theme        : 'light'    // or dark
            });
        }; 
    }

    function fetchInstas() {
        $.ajax({
            
        })
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


