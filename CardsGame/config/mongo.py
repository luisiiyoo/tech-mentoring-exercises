__MONGO_USER = 'luis'
__MONGO_PASSWORD = 'Hola1234'
__DB_NAME = 'CardsGame'

MONGO_STR_CONNECTION = f'mongodb+srv://{__MONGO_USER}:{__MONGO_PASSWORD}@wizelinecluster.r2t2n.mongodb.net/' \
                       f'{__DB_NAME}?retryWrites=true&w=majority'
