from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from items.models import ItemPage

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
        all_pages=self.get_children()
        posts=[]
        for page in all_pages:
            page_posts=ItemPage.objects.live().public().order_by('-first_published_at').child_of(page)
            for p in page_posts:
                posts.append(p)
            #posts.append(*page_posts)
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