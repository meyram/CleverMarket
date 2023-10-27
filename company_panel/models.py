from django.db import models
from django.contrib.auth.models import User
import requests

# Create your models here

public_id = 'pk_69ca9f19c6ea45ce23b28052bec43'
api_key = '81394ed8558679117135af6c57342cb7'


class Balance(models.Model):
    value = models.FloatField(default=0)
    owner = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 related_name='balance')


class Invoice(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    balance = models.ForeignKey(
        Balance,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    status = models.CharField(max_length=255,
                              default="Undefined",
                              )
    reason = models.CharField(max_length=255,
                              default="Undefined",
                              )
    text = models.TextField(
        blank=True,
        null=True,
    )
    charged = models.BooleanField(
        default=False,
    )
    from_administration = models.BooleanField(
        default=False,
    )

    def update(self, skip=True):
        if skip and self.status != "Undefined":
            return
        if self.from_administration:
            self.status = "Completed"
            self.reason = "Charge from administration"
            self.balance.value += self.value
            self.charged = 1
            self.balance.save()
            self.save()
            return

        response = requests.post(
            url='https://api.cloudpayments.ru/v2/payments/find',
            auth=(public_id, api_key),
            data={'InvoiceId': self.id}
        )
        self.text = response.text
        json_response = response.json()
        self.status = json_response['Model']['Status']
        self.reason = json_response['Model']['Reason']
        if self.status == 'Completed' and not self.charged:
            self.balance.value += self.value
            self.balance.save()
            self.charged = True
        self.save()
