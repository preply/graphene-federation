import pkg_resources
from flask import Flask


for x in ["graphql-server", "graphql-core", "flask", "graphene"]:
    print(f"{x} version is {pkg_resources.get_distribution(x).version}")


from graphql_server.flask import GraphQLView
# from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
