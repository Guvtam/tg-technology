document.addEventListener("DOMContentLoaded", () => {
    const viewport = document.querySelector(".technologies-viewport");
    const previousButton = document.querySelector(".technology-arrow-left");
    const nextButton = document.querySelector(".technology-arrow-right");

    if (!viewport || !previousButton || !nextButton) {
        console.error("No se encontraron los elementos del carrusel.");
        return;
    }

    const getStep = () => {
        const card = viewport.querySelector(".technology-card");

        if (!card) {
            return 238;
        }

        const track = viewport.querySelector(".technologies-track");
        const trackStyles = window.getComputedStyle(track);
        const gap = Number.parseFloat(trackStyles.gap) || 18;

        return card.getBoundingClientRect().width + gap;
    };

    const updateButtons = () => {
        const maximumScroll =
            viewport.scrollWidth - viewport.clientWidth;

        previousButton.disabled = viewport.scrollLeft <= 2;

        nextButton.disabled =
            viewport.scrollLeft >= maximumScroll - 2;
    };

    nextButton.addEventListener("click", () => {
        viewport.scrollBy({
            left: getStep(),
            behavior: "smooth",
        });
    });

    previousButton.addEventListener("click", () => {
        viewport.scrollBy({
            left: -getStep(),
            behavior: "smooth",
        });
    });

    viewport.addEventListener("scroll", updateButtons);

    window.addEventListener("resize", () => {
        viewport.scrollLeft = 0;
        updateButtons();
    });

    updateButtons();

    console.log(
        "Carrusel listo:",
        {
            anchoVisible: viewport.clientWidth,
            anchoTotal: viewport.scrollWidth,
        }
    );
});