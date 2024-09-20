from tortoise import fields, models


class CurrencyPair(models.Model):
    id = fields.IntField(primary_key=True)
    pair = fields.CharField(max_length=20, unique=True)
    exchange = fields.CharField(max_length=50)
    price = fields.DecimalField(max_digits=20, decimal_places=10, null=True)
    min_price = fields.DecimalField(max_digits=20, decimal_places=10, null=True)
    max_price = fields.DecimalField(max_digits=20, decimal_places=10, null=True)
    date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "currency_pairs"

    def __str__(self):
        return self.pair
