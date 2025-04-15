# from django.db import models
# from django.contrib.auth.models import User
#
# class QueryHistory(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='real_estate_queries'
#     )
#     query = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     city = models.CharField(max_length=50)
#     results_count = models.IntegerField()
#     parameters = models.JSONField(null=True, blank=True)  # Store additional query context
#
#     class Meta:
#         ordering = ['-timestamp']
#         verbose_name_plural = 'Query Histories'
#         indexes = [
#             models.Index(fields=['user', '-timestamp']),
#             models.Index(fields=['city', '-timestamp']),
#         ]
#
#     def __str__(self):
#         return f"{self.user.username}'s query on {self.city} at {self.timestamp}"