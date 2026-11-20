const contactForm = document.querySelector(".contact-form");
const contactDialog = document.querySelector(".contact-confirmation");
const homeSection = document.getElementById("inicio");

if (contactForm && homeSection && typeof contactDialog?.showModal === "function") {
    const feedback = contactForm.querySelector(".contact-feedback");
    const submitButton = contactForm.querySelector('button[type="submit"]');

    function showConfirmation() {
        const homeUrl = new URL(window.location.href);
        homeUrl.hash = "inicio";
        window.history.replaceState(window.history.state, "", homeUrl);
        homeSection.setAttribute("tabindex", "-1");
        homeSection.focus({ preventScroll: true });
        window.scrollTo({ top: 0, behavior: "instant" });
        contactDialog.showModal();
    }

    const fallback = document.querySelector(".contact-fallback");
    if (fallback) {
        fallback.hidden = true;
        showConfirmation();
    }

    contactForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        submitButton.disabled = true;
        feedback.hidden = true;

        try {
            const response = await fetch(contactForm.action, {
                method: "POST",
                headers: { Accept: "application/json" },
                body: new FormData(contactForm),
            });
            const result = await response.json();
            if (response.ok && result.saved === true) {
                contactForm.reset();
                showConfirmation();
            } else if (response.status === 422) {
                feedback.textContent = Object.entries(result.errors).flatMap(([field, errors]) => {
                    const label = contactForm.elements.namedItem(field)?.labels?.[0]?.textContent.trim();
                    return errors.map(({ message }) => label ? `${label.replace(/\s*\*$/, "")}: ${message}` : message);
                }).join(" ");
                feedback.hidden = false;
            } else {
                throw new Error("No se pudo confirmar el envío");
            }
        } catch {
            feedback.textContent = "No pudimos confirmar el envío. Conservamos lo que escribiste en el formulario.";
            feedback.hidden = false;
        } finally {
            submitButton.disabled = false;
        }
    });
}
