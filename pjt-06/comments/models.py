from django.db import models


class CommentRun(models.Model):
    query_name = models.CharField(max_length=120)
    matched_company_name = models.CharField(max_length=120, blank=True)
    stock_code = models.CharField(max_length=80, blank=True)
    original_comments = models.JSONField(default=list)
    cleaned_comments = models.JSONField(default=list)
    augmented_comments = models.JSONField(default=list)
    iqr_lower = models.FloatField(null=True, blank=True)
    iqr_upper = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def final_comments(self):
        return [*self.cleaned_comments, *self.augmented_comments]
