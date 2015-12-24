from flask import render_template, flash, g, Blueprint
from flask_login import current_user

mod_home = Blueprint('mod_home', __name__)

@mod_home.before_app_request
def before_request():
    g.user = current_user


@mod_home.route('/', methods=['GET'])
def index():


    home= """
# API paywall

Generate crypto invoices through an API which can be programatically paid using cryptocurrency. Currently only supporting NuBits

## API
All requests and responses are JSON formatted

## Registration

`GET /register`

You will be given an account number and a password. From this account you can keep track of the invoices you create.

## Account management

### Check account status

`GET /account/<account_id>`

Will return a json response with the account id if it's active.

### List all invoices

`POST /account/<account_id>/invoices`

`EXAMPLE POST: {'password':'<account_password'>}`

Will provide a list of all the invoices you've created

### Track single invoice

`POST /account/<account_id>/track/<payment_address>`

Data Required:

 * password: account password

`EXAMPLE POST: {'password':'<account_password'>}`

Will show the status of a single transaction.

### Create new invoice

`POST /account/<account_id>/new/invoice`

Data Required:

 * password: account password
 * invoice_value: integer value of invoice amount
 * currency_code: code for the currency type, currently only NBT supported

`EXAMPLE POST: {'password':'<account_password'>, "invoice_value":50, "currency_code":"nbt"}`

Creates a new invoice. Will return with an payment address.

```
EXAMPLE RESPONSE:

{
currency_code: "nbt",
invoice_value: 50,
payment_address: "BBqEyp5rEkFnjQWwqEW839BnDDaxewzMTJ"
}
```

"""

    return render_template('home/home.html', home=home)
