from django.db import models
import re
# Create your models here.
from wagtail.models import Page
from wagtail.fields import RichTextField,StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail import blocks

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class ItemPageTag(TaggedItemBase):
    content_object = ParentalKey('items.ItemPage', on_delete=models.CASCADE, related_name='tagged_items')

class ItemIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class RatingBlockValue(blocks.StructValue):
    
    @property
    def nonrating(self):
        return 10-self['rating']



class RatingBlock(blocks.StructBlock):

    rating = blocks.IntegerBlock(min_value=1,max_value=10)
    rate_comment = blocks.CharBlock(min_length=1,max_length=100)

    class Meta:
        template = 'items/rating.html'
        value_class = RatingBlockValue

class SectionBlockValue(blocks.StructValue):
    
    @property
    def nospecialtitle(self):

        return ''.join(e for e in self['title'] if e.isalnum())

class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(min_length=1,max_length=100,help_text='section title')
    richcontent = blocks.RichTextBlock(max_length=10000)
    class Meta:
        template = 'items/section.html'
        value_class = SectionBlockValue

class ItemPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    intro = StreamField([
        ('rating', RatingBlock()),
        ('text', blocks.RichTextBlock(max_length=400)),
    ], use_json_field=True)
    body =  StreamField([
        ('section', SectionBlock()),   
    ], use_json_field=True)
    tags = ClusterTaggableManager(through=ItemPageTag, blank=True)
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
        FieldPanel('body'),
        FieldPanel('feed_image'),
        FieldPanel('subject'),
        FieldPanel('tags'),
    ]

