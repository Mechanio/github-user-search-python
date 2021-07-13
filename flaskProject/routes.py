from flask import Blueprint, render_template, request
from forms import SearchForm
import json
import requests


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def home():
    searchform = SearchForm()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
            login = searchform.login.data
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
