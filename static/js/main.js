function getSongs(artist) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      var songs = JSON.parse(this.responseText);
      console.log(songs);

      // reset the slider
      document.getElementById("myRange").value = 0;

      // write in the names of the songs
      document.getElementById("song_one").innerHTML = songs[0][1];
      document.getElementById("song_two").innerHTML = songs[1][1];

      // save the id of each song, so when a choice is made we can pass that on later
      document.getElementById("song_one").title = songs[0][0];
      document.getElementById("song_two").title = songs[1][0];

      // use the album name to draw the image
      var album_name_one = songs[0][2];
      var album_name_two = songs[1][2];
      album_name_one = decodeURI(album_name_one).toLowerCase().split(" ").join("_");

      album_name_two = decodeURI(album_name_two).toLowerCase().split(" ").join("_");
      console.log(album_name_one);
      console.log(album_name_two);

      album_one_source = "/static/images/" + artist + "/" + album_name_one + ".png";
      album_two_source = "/static/images/" + artist + "/" + album_name_two + ".png";
      document.getElementById('album_one').src = album_one_source;
      document.getElementById('album_two').src = album_two_source;

      // get the elo of the song, and set it as the alt text
      var song_one_elo = songs[0][3];
      var song_two_elo = songs[1][3];
      var alt_one = "Current ELO: " + song_one_elo;
      var alt_two = "Current ELO: " + song_two_elo;
      console.log(alt_one);
      console.log(alt_two);
      document.getElementById('album_one').title = alt_one;
      document.getElementById('album_two').title = alt_two;

      var song_one_link = songs[0][4];
      var song_two_link = songs[1][4];
      document.getElementById('song_one_preview').src = song_one_link;
      document.getElementById('song_two_preview').src = song_two_link;

     }
  };
  xhttp.open("GET", "getsongs/" + artist, true);
  xhttp.send();
}
window.onload = getSongs("swift");

function buttonClicked() {
  var artist_s = document.getElementById("artist_select");
  var artist = artist_s.options[artist_s.selectedIndex].value;

  var kfactor = document.getElementById("myRange").value;

  // If kfactor is 0, then their even, don't change rankings
  // if kfactor is negative, set winner = 1
  if (kfactor != 0){
    if (kfactor < 0){
      var winner_id = document.getElementById('song_one').title;
      var loser_id = document.getElementById('song_two').title;
      // make kfactor positive
      kfactor = (-1) * kfactor;

    }else if (kfactor > 0){
      var winner_id = document.getElementById('song_two').title;
      var loser_id = document.getElementById('song_one').title;
    }else{
      alert("oh no");
    }

    var winner_info = [winner_id, loser_id, kfactor];
    console.log(winner_info);
    submitRanking(artist, winner_info);
  }else{
    getSongs(artist);
  }
}

function submitRanking(artist, textData) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      console.log("Database updated");
      getSongs(artist);
     }
  };
  xhttp.open("GET", "submitranking/" + artist + "/" + textData, true);
  xhttp.send();
}

function keyDown(event) {
  // if the user presses the "Enter" key, submit the ranking
  var key_value = event.which || event.keyCode;
  if (key_value == 13) {
    buttonClicked();
  }
}

// All subsequent code Credit to W3 Custom Select Menu
var x, i, j, l, ll, selElmnt, a, b, c;
/*look for any elements with the class "custom-select":*/
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  /*for each element, create a new DIV that will act as the selected item:*/
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /*for each element, create a new DIV that will contain the option list:*/
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < ll; j++) {
    /*for each option in the original select element,
    create a new DIV that will act as an option item:*/
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /*when an item is clicked, update the original select box,
        and the selected item:*/
        var y, i, k, s, h, sl, yl;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        sl = s.length;
        h = this.parentNode.previousSibling;
        for (i = 0; i < sl; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");

            // call getSongs on active artist
            var artist_s = document.getElementById("artist_select");
            var artist = artist_s.options[artist_s.selectedIndex].value;
            getSongs(artist);

            yl = y.length;
            for (k = 0; k < yl; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
      /*when the select box is clicked, close any other select boxes,
      and open/close the current select box:*/
      e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });
}
function closeAllSelect(elmnt) {
  /*a function that will close all select boxes in the document,
  except the current select box:*/
  var x, y, i, xl, yl, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i);
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);
