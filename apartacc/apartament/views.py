from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *



class ApartamentHome(DataMixin, ListView):
    model = Women
    template_name = 'apartament/index.html'
    context_object_name = 'posts'
    #extra_context = {'title':'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

class ApartamentCategory(DataMixin, ListView):
    model = Women
    template_name = 'apartament/index.html'
    context_object_name = 'posts'
    allow_empty = False


    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def index(request):
#     posts = Women.objects.filter(is_published = True)
#     context = {
#         'cat_selected': 0,
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница'
#     }
#     return render(request, 'apartament/index.html', context=context)

def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'apartament/about.html', {'page_obj':page_obj, 'title': 'Главная страница'})

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'apartament/addpage.html', {'form':form,'menu': menu, 'title': 'Добавление статьи'})
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'apartament/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


#def contact(request):
#    return HttpResponse("Обратная связь")
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'apartament/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')
#def login(request):
#    return HttpResponse("Авторизация")



def categories(request, catid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def archive(request, year):
    if int(year) > 2020:
        return redirect('home', permanent=False)
        #raise Http404()

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'apartament/post.html', context=context)
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'apartament/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))



# def show_category(request, cat_slug):
#     cat = Category.objects.filter(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat[0].id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#          'posts': posts,
#          'mebu': menu,
#          'title':'Главная страница',
#          'cat_selected': cat[0].id,
#      }
#     return render(request, 'apartament/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'apartament/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'apartament/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')