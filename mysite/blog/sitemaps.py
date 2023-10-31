from django.contrib.sitemaps import Sitemap
from .models import Post
# Sitemap
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priorty  = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self,obj):
        return obj.updated

