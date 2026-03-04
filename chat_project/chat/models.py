from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)

    def __self__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def __self__(self):
        return f"{self.user.name}:{self.text[:30]}"