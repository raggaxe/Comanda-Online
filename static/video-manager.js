
$('#local_vid').draggable({
  containment: 'body',
  zIndex: 10000,
  // set start position at bottom right
  start: function (event, ui) {
    ui.position.left = $(window).width() - ui.helper.width();
    ui.position.top = $(window).height() - ui.helper.height();
  },
});

function checkVideoLayout() {

  const video_grid = document.getElementById("video_grid");
  const videos = video_grid.querySelectorAll("video");
  const video_count = videos.length;

  if (video_count == 0) { } else if (video_count == 1) {
    videos[0].style.width = "100%";
    videos[0].style.height = "120px";
    videos[0].style.objectFit = "cover";
  } else if (video_count == 2) {
    videos[0].style.width = "100%";
    videos[0].style.height = "120px";
    videos[0].style.objectFit = "cover";
    videos[1].style.width = "100%";
    videos[1].style.height = "120px";
    videos[1].style.objectFit = "cover";
  } else if (video_count == 3) {
    videos[0].style.width = "100%";
    videos[0].style.height = "120px";
    videos[0].style.objectFit = "cover";
    videos[1].style.width = "100%";
    videos[1].style.height = "120px";
    videos[1].style.objectFit = "cover";
    videos[2].style.width = "100%";
    videos[2].style.height = "120px";
    videos[2].style.objectFit = "cover";
  } else {
    videos[0].style.width = "100%";
    videos[0].style.height = "120px";
    videos[0].style.objectFit = "cover";
    videos[1].style.width = "100%";
    videos[1].style.height = "120px";
    videos[1].style.objectFit = "cover";
    videos[2].style.width = "100%";
    videos[2].style.height = "120px";
    videos[2].style.objectFit = "cover";
    videos[3].style.width = "100%";
    videos[3].style.height = "120px";
    videos[3].style.objectFit = "cover";
  }
}