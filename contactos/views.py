from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ContactForm
from .models import Contact


class ContactListView(ListView):
    model = Contact
    template_name = "contactos/contact_list.html"
    context_object_name = "contacts"
    paginate_by = 8

    def get_queryset(self):
        search = self.request.GET.get("q", "").strip()
        filter_type = self.request.GET.get("filter_type", "all").strip()
        queryset = super().get_queryset()
        if search:
            if filter_type == "name":
                queryset = queryset.filter(name__icontains=search)
            elif filter_type == "email":
                queryset = queryset.filter(email__icontains=search)
            else:
                queryset = queryset.filter(Q(name__icontains=search) | Q(email__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["filter_type"] = self.request.GET.get("filter_type", "all").strip()
        context["total_contacts"] = Contact.objects.count()
        return context


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contactos/contact_form.html"
    success_url = reverse_lazy("contactos:list")

    def form_valid(self, form):
        messages.success(self.request, "El contacto se agrego correctamente.")
        return super().form_valid(form)


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contactos/contact_form.html"
    success_url = reverse_lazy("contactos:list")

    def form_valid(self, form):
        messages.success(self.request, "El contacto se actualizo correctamente.")
        return super().form_valid(form)


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contactos/contact_confirm_delete.html"
    success_url = reverse_lazy("contactos:list")

    def form_valid(self, form):
        messages.success(self.request, "El contacto se elimino correctamente.")
        return super().form_valid(form)
