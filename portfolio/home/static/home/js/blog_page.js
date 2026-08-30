// Select all blog cards
const blogCards = document.querySelectorAll(".blog-card");

blogCards.forEach((card) => {
    // When mouse enters the card
    card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-8px)";
        card.style.boxShadow = "0 10px 20px rgba(0, 0, 0, 0.15)";
        card.style.transition = "all 0.3s ease";
    });

    // When mouse leaves the card
    card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0)";
        card.style.boxShadow = "none";
    });
});