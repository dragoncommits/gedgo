from django.db import models


class Documentary(models.Model):
    class Meta:
        app_label = 'gedgo'
        verbose_name_plural = 'Documentaries'

    title = models.CharField(max_length=100, primary_key=True)
    tagline = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gedcom = models.ForeignKey('Gedcom', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)

    thumb = models.ForeignKey(
        'Document',
        related_name='documentaries_thumb',
        blank=True,
        on_delete=models.CASCADE,
    )
    tagged_people = models.ManyToManyField(
        'Person',
        related_name='documentaries_tagged_people',
        blank=True
    )
    tagged_families = models.ManyToManyField(
        'Family',
        related_name='documentaries_tagged_families',
        blank=True
    )

    def __str__(self):
        return self.title
