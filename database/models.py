from tortoise import models, fields


class User(models.Model):
    tg_id = fields.CharField(max_length=10, unique=True)
    username = fields.CharField(max_length=32, null=True)
    name = fields.CharField(max_length=129)  # 128 max chars + spacebar
    # is_admin = fields.BooleanField(default=False)
    favourite_recipes = fields.ManyToManyField('models.Recipe', related_name='favourite_by', through='userfavouriterecipe')


class Category(models.Model):
    title = fields.CharField(max_length=60)


class Recipe(models.Model):
    title = fields.CharField(max_length=60)
    url = fields.CharField(max_length=150)
    date = fields.DatetimeField(auto_now_add=True)
    category = fields.ForeignKeyField('models.Category', on_delete=fields.CASCADE, related_name='recipe_category')
    creator = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='recipe_creator')


class UserFavouriteRecipe(models.Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='user_favourites')
    recipe = fields.ForeignKeyField('models.Recipe', on_delete=fields.CASCADE, related_name='recipe_favourites')


class Report(models.Model):
    recipe = fields.ForeignKeyField('models.Recipe', on_delete=fields.CASCADE, related_name='recipe_report')
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='user_report')

