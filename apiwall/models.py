from .app import db
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=utcnow())
    date_modified = db.Column(db.DateTime,  default=utcnow(),
                                           onupdate=utcnow())

class Accounts(Base):
    __tablename__ = "accounts"

    account_id = db.Column(db.String(160))
    password_hash = db.Column(db.String(160))

    invoices = db.relationship("Invoices", backref="account")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<account {0}>'.format(self.account_id)

class Invoices(Base):
    __tablename__ = "invoices"

    ip_address = db.Column(db.String(50))
    payment_address = db.Column(db.String(50))
    currency_code = db.Column(db.String(25))
    invoice_value = db.Column(db.Float, default=0.0)
    current_value = db.Column(db.Float, default=0.0)
    payment_complete = db.Column(db.Boolean, default=False)

    transactions = db.relationship("BlockchainTransactions", backref="invoice")
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    @hybrid_method
    def blktx_total(self):
        total = 0.0

        for blkchtx in self.transactions:
            total += blkchtx.blkchtx_json.get("details")[0].get("amount")

        if self.current_value != total:
            self.current_value = total
            db.session.commit()
            return total
        return total

    @hybrid_method
    def update_total(self):
        self.blktx_total()

    @hybrid_method
    def verify_transaction(self):
        if self.blktx_total() >= self.invoice_value:
            self.payment_complete = True
            db.session.commit()

    def __repr__(self):
        return '<invoice {0}>'.format(self.id)

class BlockchainTransactions(Base):
    __tablename__ = "blockchain_transactions"

    blkchtx_id = db.Column(db.String(200))
    blkchtx_json = db.Column(JSON)

    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))

    def __repr__(self):
        return '<transaction {0}>'.format(self.id)


