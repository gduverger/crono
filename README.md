// export PATH=$PATH:/Users/gduverger/Sites/redis-4.0.6/src

redis-server &
redis-cli shutdown

# Scaling

heroku ps:scale web=1 worker=1
