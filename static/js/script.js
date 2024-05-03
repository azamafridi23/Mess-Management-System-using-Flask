const nav = document.querySelector(".nav"),
  searchIcon = document.querySelector("#searchIcon"),
  navOpenBtn = document.querySelector(".navOpenBtn"),
  navCloseBtn = document.querySelector(".navCloseBtn");
searchIcon.addEventListener("click", () => {
  nav.classList.toggle("openSearch");
  nav.classList.remove("openNav");
  if (nav.classList.contains("openSearch")) {
    return searchIcon.classList.replace("uil-search", "uil-times");
  }
  searchIcon.classList.replace("uil-times", "uil-search");
});
navOpenBtn.addEventListener("click", () => {
  nav.classList.add("openNav");
  nav.classList.remove("openSearch");
  searchIcon.classList.replace("uil-times", "uil-search");
});
navCloseBtn.addEventListener("click", () => {
  nav.classList.remove("openNav");
});
// var body = document.body;
// // Create a new div element for the background container
// var backgroundContainer = document.createElement('div');
// backgroundContainer.style.position = 'fixed';
// backgroundContainer.style.top = '0';
// backgroundContainer.style.left = '0';
// backgroundContainer.style.width = '100%';
// backgroundContainer.style.height = '100%';
// backgroundContainer.style.backgroundImage = 'url(/static/Images/login_signup_backend_image.jpg)';
// backgroundContainer.style.backgroundSize = 'cover';
// backgroundContainer.style.filter = 'blur(6px)'; // Adjust the blur intensity as needed
// backgroundContainer.style.zIndex = '-1';

// Append the background container to the body
body.appendChild(backgroundContainer);

