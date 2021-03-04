from django.contrib import admin, messages

# Register your models here.
from django.utils.html import format_html

from .models import Comments, Tags, MainContent
from .models.post import Post
from django import forms


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = ["active_post", "deactive_post"]
    filter_horizontal = ("tags",)
    exclude = ("date_pub", "comments", "like")
    list_display = ["title", "date_pub", "like_count", "comment_count"]

    # These are some method that I use in my list display
    def like_count(self, obj):
        return obj.like.all().count()

    like_count.admin_order_field = 'like'
    like_count.short_description = 'پسندیده'

    def comment_count(self, obj):
        return obj.comment.all().count()

    comment_count.admin_order_field = 'comments'
    comment_count.short_description = 'نظرات'

    """
    These are some actions that I define
    """

    def active_post(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, "پست مورد نظر فعال شد", messages.SUCCESS)

    def deactive_post(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, "پست مورد نظر غیر فعال شد", messages.SUCCESS)

    active_post.short_description = 'فعال کردن پست'
    deactive_post.short_description = 'غیر فعال کردن پست'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["text", "post_style", "like_count", "date_pub", ]
    exclude = ("date_pub", "like")
    list_display_links = ['text']

    def post_title(self):
        return self.post.title

    def post_style(self, obj):
        """
        Create a link for post in list display
        """
        url = f"/admin/blog/post/{obj.post.title}/change/"
        return format_html("<a href='{}'>{}</a>", url, obj.post)

    post_style.admin_order_field = 'post'
    post_style.short_description = 'پست'

    """
    I use this in method in my list display
    """

    def like_count(self, obj):
        return obj.like.all().count()

    like_count.admin_order_field = 'like'
    like_count.short_description = 'پسندیده'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    """
    This model is register just for admin site by using module_permission
    """
    pass


admin.site.register(MainContent)
