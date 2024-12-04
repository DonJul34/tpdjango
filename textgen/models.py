from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Define the Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.nam
    def create_default_categories():
        categories = [
            "Nature",
            "Love",
            "Fantasy",
            "Adventure",
            "Mystery",
            "Horror",
            "Science Fiction",
            "Romance",
            "Comedy",
            "Tragedy"
        ]

        for category in categories:
            Category.objects.get_or_create(name=category, description=f"Category for {category} poems.")
# Define the Poem model with a relation to Category
class Poem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poems')
    text = models.TextField()
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('fr', 'Français')], default='en')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='poems')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Poem for {self.user.username} created on {self.created_at}"

    def get_absolute_url(self):
        return reverse('poem_detail', args=[str(self.id)])

# Model to store statistics for each poem category
class PoemStatistics(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='statistics')
    number_of_poems = models.PositiveIntegerField(default=0)

    def update_statistics(self):
        # Update the number of poems for the category
        self.number_of_poems = self.category.poems.count()
        self.save()

    def __str__(self):
        return f"Statistics for {self.category.name}: {self.number_of_poems} poems"
