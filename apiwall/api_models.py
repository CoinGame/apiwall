from apiwall.models import Invoices, Accounts
from apiwall.extensions import mapi

# Marshmallow API output definitions
class InvoicesSchema(mapi.ModelSchema):
    class Meta:
        model = Invoices
        fields = ['payment_address','invoice_value','current_value','payment_complete',"currency_code",'date_created']

invoice_schema = InvoicesSchema()
invoices_schema = InvoicesSchema(many=True)

# Marshmallow API output definitions
class NewAddressSchema(mapi.ModelSchema):
    class Meta:
        model = Invoices
        fields = ['payment_address','invoice_value',"currency_code"]

newaddress_schema = NewAddressSchema()

class AccountsSchema(mapi.ModelSchema):
    class Meta:
        model = Accounts
        fields = ['account_id']

account_schema = AccountsSchema()