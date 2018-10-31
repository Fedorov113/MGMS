from django.db import models



class Tool(models.Model):
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=10, help_text='Short name used by Snakemake in Pipeline')
    version = models.CharField(max_length=256)
    home_page = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='parameters')
    short_id = models.CharField(max_length=10, help_text='Short id used by Snakemake in Pipeline')

    # JSON representation
    params = models.TextField()

    def __str__(self):
        return self.tool.name + '__' + self.short_id