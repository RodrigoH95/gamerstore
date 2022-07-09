const hamburger = document.querySelector(".hamburguer");
const navBar = document.querySelector(".nav-bar");


hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navBar.classList.toggle("active");
    document.querySelector("body").classList.toggle("active");
})