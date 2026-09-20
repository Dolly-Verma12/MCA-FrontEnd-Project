/* app.js
   -------
   Small shared helpers used across pages.
   Most page-specific interactions (water tracker, yoga popups, task
   toggles) live directly inside their own template's <script> block,
   next to the HTML they control - easier to find and edit that way.
*/

// Close any open popup when the Escape key is pressed
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    document.querySelectorAll(".overlay.active").forEach(function (el) {
      el.classList.remove("active");
    });
  }
});

// Close a popup when the dark background (outside the white box) is clicked
document.querySelectorAll(".overlay").forEach(function (overlay) {
  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) {
      overlay.classList.remove("active");
    }
  });
});
