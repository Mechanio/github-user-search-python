from flask import Blueprint, render_template, request, flash
from forms import SearchForm
from schema import schema

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def home():
    """
    Main view method of searching GitHub info via GitHub login
    :return: result of search or message about problem
    """
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
            if user_data['userInfo'] is None:
                flash('This user does not exist')
                return render_template('home.html', searchform=searchform)
            return render_template('home.html', searchform=searchform,
                                   user_info=user_data)
    return render_template('home.html', searchform=searchform)
