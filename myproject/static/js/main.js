/*
Main JavaScript file
Project-level JavaScript
*/

// Show a message when the page loads

console.log("MySite JavaScript loaded successfully.");

// Add a simple effect to navigation links

const navLinks = document.querySelectorAll(".nav-menu a");

navLinks.forEach(function(link) {

```
link.addEventListener("click", function() {

    console.log("You clicked:", link.textContent);

});
```

});
