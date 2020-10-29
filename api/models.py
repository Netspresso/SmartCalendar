from django.db import models
''' My app will be a hybrid of google calendar, todolist and notes '''


# Note model:
class Note(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    owner = models.ForeignKey('auth.User',
                              related_name='notes',
                              on_delete=models.CASCADE)

    def __str__(self):
        if self.title is None:
            return 'Note'
        else:
            return self.title


# Task model which is gonna be included by todolist
class Task(models.Model):
    '''
    A - you have to do it
    B - you don't have to fo it but it would be beneficial
    C - you don't have to do it and if you won't nothing wrong is gonna happen
    D - delegate - if someone can do it for you, delegate task to him
    E - eliminate - if somethng what are you doing causes regres - eliminate it!
    '''
    Priority_levels = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    task_name = models.CharField(max_length=160, blank=False, null=False)
    owner = models.ForeignKey('auth.User',
                              related_name='tasks',
                              on_delete=models.CASCADE)
    priority_weight = models.CharField(max_length=1,
                                       choices=Priority_levels,
                                       blank=True,
                                       null=True)
    priority_order = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.task_name, self.priority_weight,
                                 self.priority_order)
