function imageClick(album_num) {
  var radios = document.getElementsByName('album_picked');
  for (var i = 0, length = radios.length; i < length; i++) {
    if (i == album_num) {
      radios[i].checked = true
      break;
    }
  }
}

function getSongs() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      var songs = JSON.parse(this.responseText);

      // reset the checkboxes
      var radios = document.getElementsByName('album_picked');
      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
          radios[i].checked = false
          break;
        }
      }

      // reset the slider
      document.getElementById("myRange").value = 3;

      // write in the names of the songs
      document.getElementById("song_one").innerHTML = songs[0][1];
      document.getElementById("song_two").innerHTML = songs[1][1];

      // save the id of each song, so when a choice is made we can pass that on later
      document.getElementById("song_one").title = songs[0][0];
      document.getElementById("song_two").title = songs[1][0];

      // use the album name to draw the image
      var album_name_one = songs[0][2];
      var album_name_two = songs[1][2];
      album_name_one = album_name_one.toLowerCase().replace(" ", "_");
      album_name_two = album_name_two.toLowerCase().replace(" ", "_");
      album_one_source = "/static/images/"+ album_name_one + ".png";
      album_two_source = "/static/images/"+ album_name_two + ".png";
      document.getElementById('album_one').src = album_one_source;
      document.getElementById('album_two').src = album_two_source;

      // get the elo of the song, and set it as the alt text
      var song_one_elo = songs[0][3];
      var song_two_elo = songs[1][3];
      var alt_one = "Current ELO: " + song_one_elo;
      var alt_two = "Current ELO: " + song_two_elo;
      console.log(alt_one)
      console.log(alt_two)
      document.getElementById('album_one').alt = alt_one;
      document.getElementById('album_one').alt = alt_two;

      var song_one_link = songs[0][4];
      var song_two_link = songs[1][4];
      document.getElementById('song_one_preview').src = song_one_link;
      document.getElementById('song_two_preview').src = song_two_link;

     }
  };
  xhttp.open("GET", "getsongs", true);
  xhttp.send();
}
window.onload = getSongs();

function buttonClicked() {
  var radios = document.getElementsByName('album_picked');

  var winner = -1
  for (var i = 0, length = radios.length; i < length; i++) {
    if (radios[i].checked) {
      winner = radios[i].value;
      break;
    }
  }
  // if they haven't yet selected something give an error
  if (winner == -1) {
    // give user an error message or something
    return null;
  }
  var kfactor = document.getElementById("myRange").value;

  if (winner == 1){
    var winner_id = document.getElementById('song_one').title;
    var loser_id = document.getElementById('song_two').title;
  }else if (winner == 2){
    var winner_id = document.getElementById('song_two').title;
    var loser_id = document.getElementById('song_one').title;
  }else{
    alert("oh no");
  }

  var winner_info = [winner_id, loser_id, kfactor];

  submitRanking(winner_info);
}
function submitRanking(textData) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      console.log("Database updated")
      getSongs()
     }
  };
  xhttp.open("GET", "submitranking/" + textData, true);
  xhttp.send();
}
