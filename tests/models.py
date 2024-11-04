from django.db import models
from users.models import CustomUser


class TestCategory(models.Model):
    name = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'test_categories'
        
    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name='tests')

    class Meta:
        db_table = 'tests'
        
    def __str__(self):
        return self.title
    
    def get_statistics(self):
        results = self.result_set.all()
        total_users = results.values('user').distinct().count()
        total_responses = results.count()
        average_score = results.aggregate(models.Avg('score'))['score__avg'] or 0
        return {
            'total_users': total_users,
            'total_responses': total_responses,
            'average_score': average_score,
        }
        
class Result(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'results'
