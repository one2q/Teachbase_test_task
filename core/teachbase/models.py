from django.db import models


class CustomUser(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=150)
    lang = models.CharField(max_length=3, null=True, blank=True)
    external_id = models.CharField(max_length=150)
    role_id = models.IntegerField(null=True, blank=True)
    auth_type = models.IntegerField(null=True, blank=True)
    labels = models.JSONField(null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner_id = models.IntegerField()
    content_type = models.PositiveSmallIntegerField()
    owner_name = models.CharField(max_length=255)
    thumb_url = models.URLField(null=True, blank=True)
    cover_url = models.URLField(null=True, blank=True)
    description = models.TextField()
    last_activity = models.DateTimeField(auto_now=True)
    total_score = models.IntegerField()
    total_tasks = models.IntegerField()
    is_netology = models.BooleanField()
    bg_url = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    demo = models.BooleanField()
    unchangeable = models.BooleanField()
    include_weekly_report = models.BooleanField()
    custom_author_names = models.CharField(max_length=255)
    custom_contents_link = models.URLField(null=True, blank=True)
    hide_viewer_navigation = models.BooleanField()
    duration = models.TimeField(null=True, blank=True)
    account_id = models.IntegerField()


# TODO !!!!!!!!!------vvvvvvvvv
class Types(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ManyToManyField(Course)


class Author(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.IntegerField()
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=150, blank=True)
    role_id = models.SmallIntegerField()
    auth_type = models.SmallIntegerField()
    last_activity_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ManyToManyField(Course)


class Section(models.Model):
    name = models.CharField(max_length=255)
    icon_url = models.URLField(null=True, blank=True)
    small_url = models.URLField(null=True, blank=True)
    thumb_url = models.URLField(null=True, blank=True)
    icon_content_type = models.CharField(max_length=255, null=True, blank=True)
    draft = models.BooleanField(default=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )


class Materials(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ManyToManyField(Section)
    section_position = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    section_id = models.IntegerField()
    course_id = models.IntegerField()
    account_id = models.IntegerField()
    position = models.IntegerField()
    is_external = models.BooleanField()
    external_type = models.CharField(max_length=255, null=True, blank=True)
    has_file = models.BooleanField()
    extension = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_content_type = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255)
    file_size = models.IntegerField()
    size = models.IntegerField(null=True, blank=True)
    thumb_url = models.URLField(null=True, blank=True)
    view_url = models.URLField(null=True, blank=True)
    view_url_cors = models.URLField(null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    status_code = models.CharField(max_length=255)
    status_name = models.CharField(max_length=255, null=True, blank=True)
