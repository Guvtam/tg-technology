document.addEventListener("DOMContentLoaded", () => {
    const viewport = document.querySelector(".technologies-viewport");
    const track = document.querySelector(".technologies-track");

    if (!viewport || !track) {
        console.error("No se encontraron los elementos del carrusel.");
        return;
    }

    // Duplicamos las tarjetas una vez para que la animación (que se mueve
    // -50%, es decir, el ancho de un set completo) haga un loop continuo
    // sin que se note el "salto" al volver al inicio.
    const originalCards = Array.from(track.children);
    originalCards.forEach((card) => {
        const clone = card.cloneNode(true);
        clone.setAttribute("aria-hidden", "true"); // no duplicar para lectores de pantalla
        track.appendChild(clone);
    });

    // Pausa al pasar el mouse / tocar, para que se pueda leer con calma
    const pause = () => track.classList.add("is-paused");
    const resume = () => track.classList.remove("is-paused");

    viewport.addEventListener("mouseenter", pause);
    viewport.addEventListener("mouseleave", resume);
    viewport.addEventListener("touchstart", pause, { passive: true });
    viewport.addEventListener("touchend", resume);
});