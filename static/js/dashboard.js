document.addEventListener("DOMContentLoaded", function () {

    console.log("TRUESCAN Dashboard Loaded");

    // Feature cards
    const featureCards = document.querySelectorAll(".feature-card");

    featureCards.forEach(function (card) {

        card.addEventListener("click", function () {

            card.style.transform = "scale(0.98)";

            setTimeout(function () {
                card.style.transform = "";
            }, 120);

        });

    });

});