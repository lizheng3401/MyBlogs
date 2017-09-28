from django.contrib.syndication.views import Feed
from blog.models import Post

class AllPostsRssFeed(Feed):
    title = "vine 的博客"
    link = '/'
    description = 'Django 博客'

    def items(self):

        return Post.objects.all()

    def item_title(self, item):

        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):

        return item.body