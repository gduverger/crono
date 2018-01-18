py2swagger -o ~/Sites/crono/api/doc.json falcon api.main:api

export PATH=$PATH:/Users/gduverger/Sites/redis-4.0.6/src
redis-server &
