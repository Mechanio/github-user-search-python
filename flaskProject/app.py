from secrets import secret_key
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

# GraphiQL interface initialization
view_func = GraphQLView.as_view('graphql', schema=schema, graphiql=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key  # secret key in private file
app.add_url_rule('/graphql', view_func=view_func)

from routes import main

app.register_blueprint(main)

if __name__ == '__main__':
    app.run()
