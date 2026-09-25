document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", function () {

        const input = document.querySelector(
            'input[name="url"]'
        );

        if (!input || input.value.trim() === "") {
            alert("Please enter a link.");
            return;
        }

        const url = input.value.trim();

        if (!url.startsWith("http://") &&
            !url.startsWith("https://")) {

            alert("Please enter a valid URL starting with http:// or https://");
            return;
        }

    });

});