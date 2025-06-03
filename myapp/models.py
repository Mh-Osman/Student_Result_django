from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    uid = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    uid = models.PositiveIntegerField()
    roll = models.CharField(max_length=20, unique=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name


class result(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE, related_name='results')
    subject = models.CharField(max_length=100)
    mid=models.PositiveIntegerField()
    final=models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    full_mark = models.PositiveIntegerField(default=100)
    roll = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f"{self.student.name} - {self.subject}"
