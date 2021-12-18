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
    let keyword = obj.querySelector(".get-data").getAttribute("data-keywords");
    const data_url = obj.querySelector(".highlighted").getAttribute("data-url");
    keyword = keyword.split(".");
    console.log(keyword);
    console.log(data_url);
    $(`.highlighted[data-url="${data_url}"]`).mark(keyword, {
      separateWordSearch: false,
      className: "highlight",
    });
  });
});
