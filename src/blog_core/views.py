"""List / detail / preview views."""

from __future__ import annotations

from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from blog_core import conf
from blog_core.models import Article, Blog


class ArticleListView(View):
    template_name = "blog_core/article_list.html"

    def get(self, request: HttpRequest, blog_slug: str) -> HttpResponse:
        blog = get_object_or_404(Blog, slug=blog_slug, is_active=True)
        qs = (
            Article.objects.published()
            .filter(blog=blog)
            .select_related("blog", "author", "section")
        )
        paginator = Paginator(qs, conf.get_setting("PAGINATE_BY", 12))
        page = paginator.get_page(request.GET.get("page") or 1)
        return render(
            request,
            self.template_name,
            {"blog": blog, "page_obj": page, "articles": page.object_list},
        )


class ArticleDetailView(View):
    template_name = "blog_core/article_detail.html"

    def get(
        self, request: HttpRequest, blog_slug: str, slug: str
    ) -> HttpResponse:
        article = get_object_or_404(
            Article.objects.select_related("blog", "author", "section"),
            blog__slug=blog_slug,
            slug=slug,
        )
        hookset = conf.get_hookset()
        if not hookset.can_view(request, article):
            raise Http404()
        if article.is_published:
            Article.objects.filter(pk=article.pk).update(
                view_count=article.view_count + 1
            )
            article.view_count += 1
        return render(
            request,
            self.template_name,
            {
                "blog": article.blog,
                "article": article,
                "body_html": article.render_body(),
                "is_preview": False,
            },
        )


class ArticlePreviewView(View):
    """Secret-key preview for draft/scheduled articles (not listed publicly)."""

    template_name = "blog_core/article_detail.html"

    def get(
        self,
        request: HttpRequest,
        blog_slug: str,
        slug: str,
        secret_key: str,
    ) -> HttpResponse:
        article = get_object_or_404(
            Article.objects.select_related("blog", "author", "section"),
            blog__slug=blog_slug,
            slug=slug,
        )
        hookset = conf.get_hookset()
        if not hookset.can_preview_with_secret(article, secret_key):
            raise Http404()
        return render(
            request,
            self.template_name,
            {
                "blog": article.blog,
                "article": article,
                "body_html": article.render_body(),
                "is_preview": True,
            },
        )
