from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Cook, DishType, Dish
from .forms import DishSearchForm, \
    DishForm, CookExperienceUpdateForm, \
    CookCreationForm, CookSearchForm, DishTypeSearchForm, \
    IngredientForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "kitchen/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cooks"] = Cook.objects.count()
        context["num_dishes"] = Dish.objects.count()
        context["num_dish_types"] = DishType.objects.count()

        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context["num_visits"] = num_visits + 1

        return context


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 5
    queryset = Dish.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        context["search_form"] = DishSearchForm
        return context

    def get_queryset(self):
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"])
        return self.queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"
    form_class = IngredientForm

    def get_success_url(self):
        return reverse("dish_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_form'] = IngredientForm()
        return context

    def post(self, request, *args, **kwargs):
        dish = self.get_object()
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']
            dish.ingredients.set(ingredients)  # Додаємо інгредієнти до страви
            return redirect('dish_detail', pk=dish.pk)

        return self.render_to_response({'ingredient_form': form})


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5
    queryset = Cook.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        context["search_form"] = CookSearchForm
        return context

    def get_queryset(self):
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"])
        return self.queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("kitchen:cook-list",)


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5
    queryset = DishType.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        context["search_form"] = DishTypeSearchForm
        return context

    def get_queryset(self):
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"])
        return self.queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish_type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish_type-list")


class ToggleDishAssignView(LoginRequiredMixin, View):
    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        if request.user in dish.cooks.all():
            dish.cooks.remove(request.user)
        else:
            dish.cooks.add(request.user)
        return redirect(reverse("kitchen:dish-detail", args=[pk]))


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    context_object_name = "dish_type"


class AddIngredientView(LoginRequiredMixin, generic.CreateView):
    template_name = "kitchen/dish_detail.html"

    def get(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        form = IngredientForm()
        return render(
            request, self.template_name,
            {"dish": dish, "form": form})

    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredient = form.save()
            dish.ingredients.add(ingredient)
            return redirect("kitchen:dish-detail", pk=dish.pk)

        return render(
            request, self.template_name,
            {"dish": dish, "form": form})
