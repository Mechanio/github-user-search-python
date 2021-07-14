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


class UserReposQuery(graphene.ObjectType):
    repoName = graphene.String()
    repoHtmlUrl = graphene.String()


class Query(graphene.ObjectType):
    userInfo = graphene.Field(UserInfoQuery, url=graphene.String())
    userRepos = graphene.List(UserReposQuery, url=graphene.String())

    def resolve_userInfo(self, info, url):
        response = requests.get(url)
        user_data = json.loads(response.text)
        return UserInfoQuery(url=url,
                             name=user_data['name'],
                             avatarUrl=user_data['avatar_url'],
                             htmlUrl=user_data['html_url'])

    def resolve_userRepos(self, info, url):
        new_response = requests.get(url)
        user_repos = json.loads(new_response.text)
        results = []
        for i in range(len(user_repos)):
            temp = UserReposQuery(repoName=user_repos[i]['name'],
                                  repoHtmlUrl=user_repos[i]['html_url'])
            results.append(temp)
        return results


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
                                  } 
                                   userRepos(url: "https://api.github.com/users/%s/repos") {
                                    repoName
                                    repoHtmlUrl
                                  }
                                }''' % (login, login)
            user_data = schema.execute(query_user_info)
            user_data = user_data.data
            print(user_data)
            return render_template('home.html', title='GitHub Search',
                                   searchform=searchform, user_info=user_data)
    return render_template('home.html', title='GitHub Search',
                           searchform=searchform)
