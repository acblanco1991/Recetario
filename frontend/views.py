from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RecetaForm, CategoriaForm, PerfilForm, RegisterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect
from .models import *


# def author(request):
#     return HttpResponse('index.html')
# def post(request):
#     return HttpResponse('index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, first_name=first_name, password=password)
            if user is not None:
                login(request, user)  # Iniciar sesión automáticamente
                return redirect('index')  # Redirigir al usuario a la página principal
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

class index(TemplateView):
    template_name = 'index.html'
    paginate_by = 4

    def get_queryset(self):
        recetas_list = Receta.objects.all().order_by('titulo')  # Ordena por 'titulo'
        return recetas_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recetas_list = self.get_queryset()
        paginator = Paginator(recetas_list, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            recetas = paginator.page(page)
        except PageNotAnInteger:
            recetas = paginator.page(1)
        except EmptyPage:
            recetas = paginator.page(paginator.num_pages)

        context['recetas'] = recetas
        context['categorias'] = Categoria.objects.all()
        return context

class details(DetailView):
    model = Receta
    template_name = 'details.html'
    context_object_name = 'receta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_autor'] = self.request.user == self.get_object().autor
        return context

class delete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Receta
    template_name = 'delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        receta = self.get_object()
        return self.request.user == receta.autor


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor != self.request.user:
            return HttpResponseForbidden("No tienes permiso para eliminar esta receta.")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor != self.request.user:
            return HttpResponseForbidden("No tienes permiso para eliminar esta receta.")
        return super().post(request, *args, **kwargs)

class edit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Receta
    template_name = 'edit.html'
    form_class = RecetaForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if 'imagen-clear' in self.request.POST and 'imagen' in self.request.FILES:
            form.instance.imagen = self.request.FILES['imagen']
            print("Nueva imagen subida y imagen existente borrada")
        elif 'imagen' in self.request.FILES:
            form.instance.imagen = self.request.FILES['imagen']
            print("Nueva imagen subida")
        elif 'imagen-clear' in self.request.POST:
            form.instance.imagen = None
            print('imagen' in self.request.FILES)
            print(self.request.FILES)
            print("Imagen existente borrada")

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor != self.request.user:
            messages.error(request, "No tienes permiso para editar esta receta.")
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor != self.request.user:
            messages.error(request, "No tienes permiso para editar esta receta.")
            return redirect('index')
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        print("Formulario inválido")
        print(form.errors)  # Añade esto para depuración
        return super().form_invalid(form)

class add_receta(LoginRequiredMixin, CreateView):
    model = Receta
    template_name = 'add_receta.html'
    form_class = RecetaForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        if 'imagen' not in self.request.FILES:
            form.instance.imagen = '3.jpg'
        return super().form_valid(form)

class buscar_receta(ListView):
    model = Receta
    template_name = 'buscar_receta.html'
    context_object_name = 'recetas'

    def get_queryset(self):
        query = self.request.GET.get('datos', '')
        if query:
            queryset = Receta.objects.filter(titulo__icontains=query)
            if not queryset.exists():
                messages.success(self.request, '¡No hay receta con ese título!')
                return Receta.objects.none()
            return queryset
        return Receta.objects.none()

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        context['blog'] = context['object_list']  # Renombrar 'object_list' a 'blog'
        return context


class filtrar_categoria(ListView):
    model = Receta
    template_name = 'filtrar_categoria.html'
    context_object_name = 'recetas'

    def get_queryset(self):
        query = self.request.GET.get('datos', None)
        if query:
            categoria = Categoria.objects.get(nombre=query)
            queryset = Receta.objects.filter(categoria=categoria)

            if not queryset.exists():
                messages.success(self.request, '¡No hay receta con esa categoría!')

                return Receta.objects.none()
            return queryset
        return Receta.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        # context['recetas'] = Receta.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('datos', None)
        return context

class add_categoria(LoginRequiredMixin, CreateView):
    model = Categoria
    template_name = 'add_categoria.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('index')

class details_categoria(DetailView):
    model = Categoria
    template_name = 'details_categoria.html'

class delete_categoria(DeleteView):
    model = Categoria
    template_name = 'delete_categoria.html'
    success_url = reverse_lazy('index')

class edit_categoria(UpdateView):
    model = Categoria
    template_name = 'edit_categoria.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('index')


class details_perfil(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'details_perfil.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

class edit_perfil(UpdateView):
    model = User
    form_class = PerfilForm
    template_name = 'edit_perfil.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def get_object(self):
        return self.request.user
        # return User.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)

class delete_perfil(DeleteView):
    model = User
    template_name = 'delete_perfil.html'
    success_url = reverse_lazy('index')