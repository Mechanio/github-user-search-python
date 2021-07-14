from flask import Blueprint, render_template, request
from forms import SearchForm
from schema import schema

main = Blueprint('main', __name__)


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
            return render_template('home.html', title='GitHub Search',
                                   searchform=searchform, user_info=user_data)
    return render_template('home.html', title='GitHub Search',
                           searchform=searchform)
