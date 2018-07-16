from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50, )
    description = models.CharField(max_length=200, default="")
    content = models.CharField(max_length=5000)
    date_publish = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_publish']

    def __str__(self):
        return self.title

# ALTER TABLE  `blog_article` CHANGE  `date_publish`  `date_publish` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP