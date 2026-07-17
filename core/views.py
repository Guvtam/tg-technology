from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactRequestForm


def home(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                (
                    "Tu solicitud fue enviada correctamente. "
                    "Me pondré en contacto contigo a la brevedad."
                ),
            )

            return redirect("core:home")
    else:
        form = ContactRequestForm()

    return render(
        request,
        "core/home.html",
        {
            "contact_form": form,
        },
    )