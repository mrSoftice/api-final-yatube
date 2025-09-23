from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Текст публикации')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return (
            f'{self.text[:128]}\n'
            f'Author: {self.author}\n'
            f'Published: {self.pub_date.strftime("%Y-%m-%d %H:%M:%S")}'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('текст комментария')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='following'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(user=models.F('following')),
                name='prevent_self_follow'
            ),
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_follow'
            ),
        ]
