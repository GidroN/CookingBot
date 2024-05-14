from tortoise import models, fields


class User(models.Model):
    tg_id = fields.CharField(max_length=10, unique=True)
    username = fields.CharField(max_length=32, null=True)
    name = fields.CharField(max_length=129)  # 128 max chars + spacebar
    # is_admin = fields.BooleanField(default=False)
    favourite_receipts = fields.ManyToManyField('models.Receipt', related_name='favourite_by', through='')


class Category(models.Model):
    title = fields.CharField(max_length=60)


class Receipt(models.Model):
    title = fields.CharField(max_length=60)
    url = fields.CharField(max_length=150)
    category = fields.ForeignKeyField('models.Category', on_delete=fields.CASCADE, related_name='receipt_category')
    creator = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='receipt_creator')


class UserFavouriteReceipt(models.Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name='user_favourites')
    receipt = fields.ForeignKeyField('models.Receipt', on_delete=fields.CASCADE, related_name='receipt_favourites')
