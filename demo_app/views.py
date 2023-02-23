from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.conf import settings

from django_filters.views import FilterView

from .models import Car
from .models import BuyersRequest
from .forms import BuyersRequestForm
from .forms import ListCarForm
from .filter import CarFilter


class CarListView(FilterView):
    """
    Home page - contains List of cars with paginations and filter
    """

    model = Car
    template_name = "home.html"
    ordering = ["id"]
    paginate_by = 10
    filterset_class = CarFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        make = self.request.GET.get("make", None)
        year = self.request.GET.get("year", None)
        if make and year:
            queryset = queryset.filter(make=make, year=year)
        return queryset

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["filter"] = CarFilter(
                self.request.GET, queryset=self.get_queryset()
            )
            return context

        except Exception as e:
            self.kwargs["page"] = 1
            #return super(CarListView, self).get_context_data(**kwargs)
            return super().get_context_data(**kwargs)



class AddCarFormView(FormView):
    """
    Seller can list there car.
    """

    template_name = "listform.html"
    form_class = ListCarForm

    def form_valid(self, form):
        form.save(self.request.user)
        return super(AddCarFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("addcar")


class AdminLoginView(LoginView):
    """
    Login page - only admin can logged in
    """

    template_name = "login.html"

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.add_message(self.request, messages.ERROR,
                             "Invalid Credentials.")
        return super().form_invalid(form)


class BuyFormView(CreateView, FormView):
    """
    Buy page - for purchasing the listed car.
    """

    template_name = "buyform.html"
    form_class = BuyersRequestForm
    success_url = reverse_lazy("thankyou")

    def form_valid(self, form, **kwargs):
        context_data = self.get_context_data(form=form, **kwargs)
        car = Car.objects.filter(uid=context_data["cid"].replace("-", "")).first()
        form.instance.car = car
        car.is_sold = True
        car.save()

        # for sending email
        mail_template = get_template("email.html")
        commission = int(car.price.amount) * 5 / 100
        net_amount = (car.price.amount) - int(commission)
        data = {
            "car": car,
            "buyerreq_obj": BuyersRequest,
            "commission": commission,
            "net_amount": net_amount,
        }
        html_content = mail_template.render(data)
        # send_mail(subject='New car purchase request at Dodgy Bros',
        # message='New purchase request', from_email=settings.EMAIL_FROM,
        # recipient_list=[settings.EMAIL_TO], html_message=html_content)

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(BuyFormView, self).get_context_data(*args, **kwargs)
        cid = self.kwargs.get("cid")
        context["cid"] = cid
        return context

class ThanksTemplateView(TemplateView):
    template_name = "success.html"

class MakeCarAvailableView(LoginRequiredMixin, DetailView):
    """
    Make sold out car available - only logged in can use this.
    """

    model = Car
    template_name = "home.html"
    slug_url_kwarg = "cid"
    slug_field = "uid"

    def get_context_data(self, *args, **kwargs):
        context = super(MakeCarAvailableView, self).get_context_data(*args, **kwargs)
        car = kwargs.get("object")
        car.is_sold = False
        car.save()
        return context

    def get_success_url(self):
        return reverse("thankyou")
