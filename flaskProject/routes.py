from flask import Blueprint, render_template, request
from forms import SearchForm
import json
import requests
import graphene

main = Blueprint('main', __name__)


class UserInfoQuery(graphene.ObjectType):
    url = graphene.String()
    name = graphene.String()
    avatarUrl = graphene.String()
    htmlUrl = graphene.String()
    reposUrl = graphene.String()


class Query(graphene.ObjectType):
    userInfo = graphene.Field(UserInfoQuery, url=graphene.String())

    def resolve_userInfo(self, info, url):
        response = requests.get(url)
        user_data = json.loads(response.text)
        return UserInfoQuery(url=url,
                             name=user_data['name'],
                             avatarUrl=user_data['avatar_url'],
                             htmlUrl=user_data['html_url'],
                             reposUrl=user_data['repos_url'])


schema = graphene.Schema(query=Query)


@main.route('/', methods=['GET', 'POST'])
def home():
    searchform = SearchForm()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            login = searchform.login.data
            query_user_info = '''{
                                   userInfo(url: "https://api.github.com/users/%s") {
                                    name
                                    url
                                    avatarUrl
                                    htmlUrl
                                    reposUrl
                                  }
                                }''' % login
            user_data = schema.execute(query_user_info)
            user_data = user_data.data
            print(user_data)
            response = requests.get(user_data['userInfo']['reposUrl'])
            user_repos = json.loads(response.text)
            repos_names_urls = {}
            for repo in user_repos:
                repos_names_urls[repo['name']] = repo['html_url']
            return render_template('home.html', title='GitHub Search',
                                   searchform=searchform, repos_names_urls=repos_names_urls,
                                   user_info=user_data)
    return render_template('home.html', title='GitHub Search',
                           searchform=searchform)
