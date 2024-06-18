const hamMenu = document.querySelector(".hamburger");

const offScreenMenu = document.querySelector(".off-screen-menu");

const login = document.querySelector("sign-in-button");
const register = document.querySelector("sign-in-button");

hamMenu.addEventListener("click", () => {
  hamMenu.classList.toggle("active");
  offScreenMenu.classList.toggle("active");
});

login.addEventListener("hover", () => {
  this.style.backgroundColor = "red";
 });
