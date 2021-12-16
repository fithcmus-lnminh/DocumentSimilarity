function toggle(id) {
  let cardHeader = document.getElementById(id);
  console.log(cardHeader);
  let card = cardHeader.parentElement;
  console.log(card);
  let cardBody = card.querySelector(".card-body");
  console.log(cardBody);

  cardBody.classList.toggle("active");
}
