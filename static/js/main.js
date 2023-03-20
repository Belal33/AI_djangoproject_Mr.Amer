let slidButtons = document.querySelectorAll("button.next-section");
let slidPage = document.querySelector(".page");
let sections = document.querySelectorAll("section")

slidPage.style.setProperty("left", "0%");
slidButtons.forEach((el, i) => {
  el.addEventListener("click", () => {
    if (i < sections.length - 1) {
      slidPage.style.setProperty("left", -100 * (i + 1) + "%");
      console.log(slidPage.style.getPropertyValue("left"));
    }
  });
});


let response = document.querySelector(".response")

if (response.textContent.trim()== "") {
  response.style.setProperty("border", "none");
}