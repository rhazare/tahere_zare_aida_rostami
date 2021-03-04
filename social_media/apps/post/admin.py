from django.contrib import admin, messages

# Register your models here.
from django.utils.html import format_html

from .models import Comments
from .models.post import Post
from django import forms


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = ["confirm_post", "active_post", "reject_post", "deactive_post"]
    readonly_fields = ["confirm"]
    filter_horizontal = ("tags",)
    exclude = ("date_pub", "dislike", "comments", "like")
    list_display = ["title", "confirm", "date_pub", "user_style", "like_count", "dislike_count", "comment_count"]

    #These are some method that I use in my list display
    def like_count(self, obj):
        return obj.like.all().count()

    like_count.admin_order_field = 'like'
    like_count.short_description = 'پسندیده'

    def dislike_count(self, obj):
        return obj.dislike.all().count()

    dislike_count.admin_order_field = 'dislike'
    dislike_count.short_description = 'نپسندیده'

    def comment_count(self, obj):
        return obj.comment.all().count()

    comment_count.admin_order_field = 'comments'
    comment_count.short_description = 'نظرات'

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     For initial writer of post in form with out asking a user in admin
    #     """
    #     form = super().get_form(request, obj, **kwargs)
    #     if request.user.has_perm('blog.add_post'):
    #         form.base_fields['user'].initial = request.user
    #     disabled_fields = ('user',)
    #     for item in disabled_fields:
    #         if item in form.base_fields:
    #             form.base_fields[item].disabled = True
    #             form.base_fields[item].widget = forms.HiddenInput()
    #
    #     return form

    def user_style(self, obj):
        url = f"/admin/auth/user/{obj.user.pk}/change/"
        return format_html("<a href='{}'>{}</a>", url, obj.user.first_name + " " + obj.user.last_name)

    user_style.admin_order_field = 'user'
    user_style.short_description = 'کاربر'

    def get_actions(self, request):
        """
        handle the given action by checking the permission  of request.user
        """
        actions = super().get_actions(request)
        if request.user.has_perm("blog.confirm_post") is False:
            if 'confirm_post' in actions:
                del actions['confirm_post']
                del actions['reject_post']
        if request.user.has_perm("blog.active_post") is False:
            if 'active' in actions:
                del actions['active']
                del actions['deactive']
        return actions

    def get_queryset(self, request):
        """
        Handle that the writer can see just his or her post in his or her admin panel

        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.has_perm("blog.confirm_post"):
            return qs
        elif request.user.has_perm("blog.add_post"):
            self.list_display = ["title", "confirm", "active", "date_pub"]
            return qs.filter(user=request.user)

    """
    These are some actions that I define
    """

    def reject_post(self, request, queryset):
        queryset.update(confirm=False)
        self.message_user(request, "پست مورد نظر رد شد", messages.SUCCESS)

    def confirm_post(self, request, queryset):
        queryset.update(confirm=True)
        self.message_user(request, "پست مورد نظر تایید شد", messages.SUCCESS)

    def active_post(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, "پست مورد نظر فعال شد", messages.SUCCESS)

    def deactive_post(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, "پست مورد نظر غیر فعال شد", messages.SUCCESS)

    reject_post.short_description = 'رد کردن پست'
    confirm_post.short_description = 'تایید کردن پست'
    active_post.short_description = 'فعال کردن پست'
    deactive_post.short_description = 'غیر فعال کردن پست'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    actions = ["confirm_comment", "reject_comment"]
    list_display = ["text", "post_style", "confirm", "like_count", "dislike_count", "date_pub", ]
    readonly_fields = ["confirm"]
    exclude = ("date_pub", "like", "dislike")
    list_display_links = ['text']

    def has_module_permission(self, request):
        """
        For registering this model in admin just for person how can confirm the comment
        For instance for writer this model is not register
        """
        if request.user.has_perm('blog.confirm_post'):
            return True
        else:
            return False

    def post_title(self):
        return self.post.title

    def post_style(self, obj):
        """
        Create a link for post in list display
        """
        url = f"/admin/blog/post/{obj.post.pk}/change/"
        return format_html("<a href='{}'>{}</a>", url, obj.post)

    post_style.admin_order_field = 'post'
    post_style.short_description = 'مطلب'

    def get_queryset(self, request):
        """
         Handle that the writer can see just his or her post comment in his or her admin panel
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.has_perm("blog.confirm_comment"):
            return qs
        elif request.user.has_perm("blog.view_comments"):
            return qs.filter(post__user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        """
        For initial writer of comment in form with out asking a user in admin
        """
        form = super().get_form(request, obj, **kwargs)
        if request.user.has_perm('blog.add_comments'):
            form.base_fields['user'].initial = request.user
        disabled_fields = ('user',)
        for item in disabled_fields:
            if item in form.base_fields:
                form.base_fields[item].disabled = True
                form.base_fields[item].widget = forms.HiddenInput()

        return form

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.has_perm("blog.confirm_comment") is False:
            if 'confirm_comment' in actions:
                del actions['confirm_comment']
                del actions['reject_comment']
        return actions

    """
    These are some actions that I define
    """

    def confirm_comment(self, request, queryset):
        queryset.update(confirm=True)
        self.message_user(request, "پست مورد نظر تایید شد", messages.SUCCESS)

    def reject_comment(self, request, queryset):
        queryset.update(confirm=False)
        self.message_user(request, "پست مورد نظر رد شد", messages.SUCCESS)
    """
    I use this in method in my list display
    """
    def like_count(self, obj):
        return obj.like.all().count()

    like_count.admin_order_field = 'like'
    like_count.short_description = 'پسندیده'

    def dislike_count(self, obj):
        return obj.dislike.all().count()

    dislike_count.admin_order_field = 'dislike'
    dislike_count.short_description = 'نپسندیده'
    confirm_comment.short_description = 'تایید کردن نظر'
    reject_comment.short_description = 'رد کردن نظر'

