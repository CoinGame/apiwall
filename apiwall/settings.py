# -*- coding: utf8 -*-
import os
import logging as dlog
basedir = os.path.abspath(os.path.dirname(__file__))
logdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'logs'))

#Logging configration
logfile = os.path.join(logdir,'debug.log')
dlog.basicConfig(filename=logfile,level=dlog.DEBUG,format="[%(levelname)s] %(asctime)s.%(msecs)dGMT %(module)s - %(funcName)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


class Config(object):
    LIVESERVER_PORT = 8000

    BASE_DIR = basedir

    if os.environ.get('APIWALL_SECRET_KEY'):
        SECRET_KEY = os.environ.get('APIWALL_SECRET_KEY')
    else:
        SECRET_KEY = "this_should_only_be_used_in_testing"

    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = ('postgresql:///apiwalldev')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    SQLALCHEMY_RECORD_QUERIES = True

    if os.environ.get('APIWALL_DB_USER'):
        APIWALL_DB_USER = os.environ.get('APIWALL_DB_USER')
    else:
        APIWALL_DB_USER = "postgres"

    if os.environ.get('APIWALL_DB_USER_PASSWORD'):
        APIWALL_DB_USER_PASSWORD = os.environ.get('APIWALL_DB_USER_PASSWORD')
    else:
        APIWALL_DB_USER_PASSWORD = "test"

    #RPC INFO
    configfile = '{0}/.{1}/{2}'.format(os.getenv("HOME"),"nushadow","nushadow.conf")
    walletconfig= dict(tuple(line.strip().replace(' ','').split('=')) for line in open(configfile).readlines())

    RPC_USER = walletconfig.get("rpcuser")
    RPC_PASSWORD = walletconfig.get("rpcpassword")

    if walletconfig.get("rpcport"):
        RPC_PORT = walletconfig.get("rpcport")
    else:
        RPC_PORT = 14011

class ProdConfig(Config):
    ENV = "prod"
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = ('postgresql:///apiwallproduction')
    LIVESERVER_PORT = 80

class StagingConfig(Config):
    ENV = "staging"
    TESTING = False
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = ('postgresql:///apiwalldev')

class DevConfig(Config):
    ENV = "dev"
    TESTING = False
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = ('postgresql:///apiwalldev')

class TestConfig(Config):
    ENV = "test"
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = ('postgresql:///apiwalltest')
