from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


class List(models.Model):
    name = models.CharField(max_length=40)
    date_created = models.DateTimeField("date created", default=timezone.now)
    date_updated = models.DateTimeField("date updated", default=timezone.now)

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='lists_owned'
    )
    contributors = models.ManyToManyField(
        CustomUser,
        related_name='lists_contributed'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["date_updated"]

    def serialize_rows(self):
        rows = []
        for row in self.rows.all():
            rows.append({
                'id': row.id,
                'added_by': row.added_by.username,
                'date_added': row.date_added.strftime("%d-%m-%Y"),
                'title': row.title,
                'media_type': row.get_media_type_display(),

                # invisible
                'imdb_url': row.imdb_url,
            })
        return rows


class MediaListRow(models.Model):
    MEDIA_TYPES = [
        ('movie', 'Movie'),
        ('tv', 'Series'),
    ]

    title = models.CharField(max_length=80)
    imdb_url = models.URLField(blank=True)
    date_added = models.DateTimeField("date added", default=timezone.now)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPES,
        null=False
    )
    appears_in = models.ForeignKey(
        List,
        on_delete=models.CASCADE,
        related_name="rows"
    )
