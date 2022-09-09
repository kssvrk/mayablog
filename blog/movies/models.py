from django.db import models

# Create your models here.
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class MoviePageTag(TaggedItemBase):
    content_object = ParentalKey('movies.MoviePage', on_delete=models.CASCADE, related_name='tagged_items')

class MovieIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class MoviePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    subject = models.CharField(max_length=250,default='Movie')
    rating = models.IntegerField(null=True,blank=True,choices=[(i, i) for i in range(1, 11)])
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=MoviePageTag, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('rating'),
        FieldPanel('body'),
        FieldPanel('feed_image'),
        FieldPanel('subject'),
        FieldPanel('tags'),
    ]

    @property
    def get_nonrating(self):
        
        return 10-self.rating