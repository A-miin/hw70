from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode

from article.models import Article
from article.forms import ArticleForm, SearchForm


class IndexView(ListView):
    """
    Представление для просмотра списка статей. Представление реализовано с
    использованием generic-представления ListView.

    В представлении активирована пагинация и реализован поиск
    """
    template_name = 'articles/index.html'
    model = Article
    context_object_name = 'articles'
    ordering = ('title', '-created_at')
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexView, self).get(request, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(title__icontains=self.search_data) |
                Q(author__icontains=self.search_data) |
                Q(content__icontains=self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context


class ArticleView(DetailView):
    model = Article
    template_name = 'articles/view.html'


class CreateArticleView(CreateView):
    template_name = 'articles/create.html'
    form_class = ArticleForm
    model = Article
    success_url = reverse_lazy('article-list')

    def form_valid(self, form):
        tags = form.cleaned_data.pop('tags')
        article = Article()
        for key, value in form.cleaned_data.items():
            setattr(article, key, value)

        article.save()
        article.tags.set(tags)

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'articles/update.html'
    context_object_name = 'article'

    def get_success_url(self):
        return reverse('article-view', kwargs={'pk': self.kwargs.get('pk')})


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'articles/delete.html'
    context_object_name = 'article'
    success_url = reverse_lazy('article-list')
