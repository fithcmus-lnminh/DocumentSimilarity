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
  const result = document.querySelectorAll(".result-card");
  Array.from(result).forEach((obj) => {
    let sentence = obj.querySelector(".get-data").getAttribute("data-keywords");
    const data_url = obj.querySelector(".highlighted").getAttribute("data-url");
    sentence = sentence.split(".");

    $(`.highlighted[data-url="${data_url}"]`).mark(sentence, {
      separateWordSearch: false,
      className: "highlight",
    });
  });
});
