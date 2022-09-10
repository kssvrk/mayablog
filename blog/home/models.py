from django.db import models
from django.conf import settings
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from items.models import ItemPage

from django.contrib.auth import get_user_model
User=get_user_model()

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    template = "items/item_index_page.html"

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        #all_posts = ItemPage.objects.live().public().order_by('-first_published_at')
        
        
        posts=ItemPage.objects.live().public().order_by('-first_published_at')
            

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            posts = posts.filter(tags__slug__in=[tags])
            context['tag']=tags
        if request.GET.get('author', None):
            owner = request.GET.get('author')
            user=User.objects.get(username=owner)
            posts = posts.filter(owner=user)
            context['author']=owner
        
        # Paginate all posts by 2 per page
        paginator = Paginator(posts, 50)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        
        return context