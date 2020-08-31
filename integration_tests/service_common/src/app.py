from flask import Flask

from graphql_server.flask import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema.graphql_schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
