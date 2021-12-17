function toggle(id) {
  let cardHeader = document.getElementById(id);
  let card = cardHeader.parentElement;
  let cardBody = card.querySelector(".card-body");

  cardBody.classList.toggle("active");
}

function showLoading() {
  $("#loading-spinner").css("display", "block");
}

$().ready(function () {
  const result = document.getElementsByClassName("result-card");

  //for (let i = 0; i < result.length; i++) {
  const keyword = $(".get-data").attr("data-keywords");
  const data_url = $(".highlighted").attr("data-url");
  console.log(keyword);

  $(`.highlighted[data-url="${data_url}"]`).mark(keyword, {
    separateWordSearch: false,
  });
  // }
});
