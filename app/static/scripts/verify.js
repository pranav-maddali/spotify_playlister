function checkInput(num_tracks) {
  var btn = document.getElementById("btn");
  var x = num_tracks.value;
  if (isNaN(x)) {
    btn.className = "hidden";
  } else {
    btn.className = "unhidden";
  }
  if (x >= 1 && x <= 19) {
    btn.className = "unhidden";
  } else {
    btn.className = "hidden";
  }
};

function preloader() {
  var item = document.getElementById("loader");
  if (item.className == "hidden") {
    item.className = "unhidden";
    document.getElementById("create_text").style.display = "none";
  }
};
