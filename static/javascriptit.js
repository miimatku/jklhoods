// Javascript source code
window.onload = function(){
	alustus();
	twitteriStriimi();
}

function alustus() {
    $("#show_twitter").click(show_twitter);
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
        }).then (function (el) {
      el.contentDocument.querySelector(".footer").style.display = "none";
    });
    }; 
}

function show_twitter(e){
	e.preventDefault();
	$("#div_insta").hide();
	$("#div_twitter").removeClass("");
}

