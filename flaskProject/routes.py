from flask import Blueprint, render_template, request
from forms import SearchForm
import json
import requests
import graphene
import extraction

main = Blueprint('main', __name__)


class UserInfoQuery(graphene.ObjectType):
    url = graphene.String()
    name = graphene.String()
    avatar_url = graphene.String()
    html_url = graphene.String()


class Query(graphene.ObjectType):
    userInfo = graphene.Field(UserInfoQuery, url=graphene.String())

    def resolve_userInfo(self, info, url):
        response = requests.get(url)
        user_data = json.loads(response.text)
        return UserInfoQuery(url=url,
                             name=user_data['name'],
                             avatar_url=user_data['avatar_url'],
                             html_url=user_data['html_url'])


schema = graphene.Schema(query=Query)


@main.route('/', methods=['GET', 'POST'])
def home():
    searchform = SearchForm()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            login = searchform.login.data
            query = '{ name }'
            result = schema.execute(query)
            print(result)
            response = requests.get(f'https://api.github.com/users/{login}')
            user_data = json.loads(response.text)
            response = requests.get(user_data['repos_url'])
            user_repos = json.loads(response.text)
            user_info = {'name': user_data['name'], 'avatar': user_data['avatar_url'],
                         'html_url': user_data['html_url']}
            repos_names_urls = {}
            for repo in user_repos:
                repos_names_urls[repo['name']] = repo['html_url']
            return render_template('home.html', title='GitHub Search',
                                   searchform=searchform, repos_names_urls=repos_names_urls,
                                   user_info=user_info)
    return render_template('home.html', title='GitHub Search',
                           searchform=searchform)
