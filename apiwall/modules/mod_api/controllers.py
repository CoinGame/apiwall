import uuid, string, random, logging
from flask import render_template, flash, g, Blueprint, request, jsonify, json, Response
from flask_login import current_user
from apiwall.blockchainrpc import RPC
from apiwall.settings import Config
from apiwall.database import db
from apiwall.models import Invoices, Accounts
from apiwall.api_models import invoices_schema, invoice_schema, newaddress_schema, account_schema

mod_api = Blueprint('mod_api', __name__)

@mod_api.before_app_request
def before_request():
    g.user = current_user

@mod_api.route('/register', methods=['GET'])
def registration():

    if request.method == 'GET':

        account = uuid.uuid4().hex
        password = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(40))

        newaccount = Accounts(account_id=account)
        newaccount.set_password(password)
        db.session.add(newaccount)
        db.session.commit()

        return json.dumps({'account_id':account,'password':password})

    return json.dumps({"error":"you need to GET here"}), 400

@mod_api.route('/account/<accountid>', methods=['POST','GET'])
def account(accountid):

    account = Accounts.query.filter_by(account_id = accountid).first()

    if account:
        return account_schema.jsonify(account)
    else:
        return json.dumps({"error":"invalid account"}), 400

@mod_api.route('/account/<accountid>/new/invoice', methods=['GET','POST'])
def account_new_transaction(accountid):

    account = Accounts.query.filter_by(account_id = accountid).first()

    if account:

        if request.method == 'POST':

            #check to see if its valid json first
            try:
                data = json.loads(request.data)
            except ValueError:
                return json.dumps({"error":"bad json"}), 400

            if 'password' in data:
                if 'invoice_value' in data:
                    if 'currency_code' in data:
                        if account.check_password(data.get("password")):
                            rpc = RPC(url="http://{0}:{1}@localhost:{2}".format(Config.RPC_USER, Config.RPC_PASSWORD, Config.RPC_PORT))

                            address = rpc.call("getnewaddress")

                            invoice = Invoices()
                            invoice.payment_address = address
                            invoice.account = account
                            invoice.currency_code = data.get('currency_code')
                            invoice.ip_address =  request.remote_addr
                            invoice.invoice_value = data.get("invoice_value")

                            db.session.add(invoice)
                            db.session.commit()

                            return newaddress_schema.jsonify(invoice)
                        else:
                            return json.dumps({"error":"bad password"}), 400
                    else:
                        return json.dumps({"error":"missing currency_code"}), 400
                return json.dumps({"error":"missing invoice_value"}), 400
            else:
                return json.dumps({"error":"missing password"}), 400

        return json.dumps({"error":"you need to post here"}), 400

    else:
        return json.dumps({"error":"invalid account"}), 400

@mod_api.route('/account/<accountid>/track/<invoiceddress>', methods=['GET','POST'])
def account_track_transaction(accountid, invoiceddress):

    account = Accounts.query.filter_by(account_id = accountid).first()

    if account:
        if request.method == 'POST':
            #check to see if its valid json first
            try:
                data = json.loads(request.data)
            except ValueError:
                return json.dumps({"error":"bad json"}), 400

            if 'password' in data:
                if account.check_password(data.get("password")):
                    invoice = Invoices.query.filter_by(payment_address = invoiceddress).first_or_404()

                    if invoice.payment_complete is False:
                        invoice.verify_transaction()
                    else:
                        invoice.update_total()

                    return invoice_schema.jsonify(invoice)
                else:
                    return json.dumps({"error":"bad password"}), 400
            else:
                return json.dumps({"error":"missing password"}), 400
        else:
            return json.dumps({"error":"you need to post here"}), 400
    else:
        return json.dumps({"error":"invalid account"}), 400

@mod_api.route('/account/<accountid>/invoices', methods=['GET','POST'])
def acount_transactions(accountid):

    account = Accounts.query.filter_by(account_id = accountid).first()

    if account:
        if request.method == 'POST':

            #check to see if its valid json first
            try:
                data = json.loads(request.data)
            except ValueError:
                return json.dumps({"error":"bad json"}), 400

            if 'password' in data:
                if account.check_password(data.get("password")):

                    invoices = invoices_schema.dump(account.transactions)

                    return Response(json.dumps(invoices.data),  mimetype='application/json')
                else:
                    return json.dumps({"error":"bad password"}), 400
            else:
                return json.dumps({"error":"missing password"}), 400
        else:
            return json.dumps({"error":"you need to post here"}), 400
    else:
        return json.dumps({"error":"invalid account"}), 400
