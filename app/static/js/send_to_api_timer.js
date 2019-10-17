var counter = 60;


setTimeout(function(){
    // var data = document.getElementById("data").innerHTML

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/send-data', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({}));
    console.log(xhr.response, xhr.status)
    var response = JSON.parse(xhr.response)
    window.location.href = response['redirect']

}, counter * 1000);

var interval = setInterval(function() {
    counter--;
    if (counter <= 0) {
     		clearInterval(interval); 
        return;
    }else{
      var t = document.getElementById('timer')
    	t.innerHTML = counter.toString()
      // console.log("Timer --> " + counter)
    }
}, 1000);