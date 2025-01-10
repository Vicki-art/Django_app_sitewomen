from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.shortcuts import render
from .utils import DataMixin
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.core.cache import cache
from .models import Women, TagPost, UploadFiles
from .forms import AddPostForm, UploadFileForm, ContactForm


class MainPage(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Main page'
    cat_selected = 0

    def get_queryset(self):
        w_lst = cache.get('women_posts')
        if not w_lst:
            w_lst = Women.published.all().select_related('cat')
            cache.set('women_posts', w_lst, 60)

        return w_lst


def handle_uploaded_file(f):
    with open(f'uploads/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    data = {'title': 'About', 'form': form}

    return render(request, 'women/about.html', data)


class AddPost(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    permission_required = 'women.add_women'

    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('add_page')
    title_page = 'Adding new page'
    login_url = '/users/login/'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePost(PermissionRequiredMixin, DataMixin, UpdateView):
    permission_required = 'women.change_women'

    model = Women
    fields = ['title', 'content', 'photo', 'cat', 'husband', 'is_published']
    template_name = 'women/editpage.html'
    success_url = reverse_lazy('index')
    title_page = 'Page editing'


class DeletePost(DataMixin, DeleteView):
    model = Women
    template_name = 'women/deletepage.html'
    success_url = reverse_lazy('index')
    title_page = 'Delete page'


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('index')
    title_page = 'Feedback'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


def login(request):
    return HttpResponse('Авторизация')


# GET POST (CBV)
class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self):
        return Women.published.get(slug=self.kwargs['post_slug'])


# GET POSTS LIST ON CATEGORY (CBV)
class ShowCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        print(cat.pk)
        return self.get_mixin_context(context,
                                      title='Category - ' + cat.name,
                                      cat_selected=cat.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')


# GET POSTS LIST ON TAG (CBV)
class ShowTagPostlist(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tag__slug=self.kwargs['tag_slug'])  # .select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = TagPost.objects.filter(slug=self.kwargs['tag_slug'])[0].tag
        return self.get_mixin_context(context, title='Tag - ' + tag_name)
