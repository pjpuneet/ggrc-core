# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

DEBUG = True
TESTING = True
PRODUCTION = False
HOST = '0.0.0.0'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@localhost/ggrcdevtest'
FULLTEXT_INDEXER = 'ggrc.fulltext.mysql.MysqlIndexer'
LOGIN_MANAGER = 'ggrc.login.noop'
#SQLALCHEMY_ECHO = True
