from app import app
from schema import schema


class TestViews:
    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def teardown(self):
        pass


class TestRequests:
    def test_home_request(self):
        query_user_info = '''{
                               userInfo(url: "https://api.github.com/users/torvalds") {
                                name
                                url
                                avatarUrl
                                htmlUrl
                              } 
                               userRepos(url: "https://api.github.com/users/torvalds/repos") {
                                repoName
                                repoHtmlUrl
                              }
                            }'''
        user_data = schema.execute(query_user_info)
        user_data = user_data.data
        assert user_data['userInfo']['name'] == 'Linus Torvalds'
        assert user_data['userInfo']['htmlUrl'] == 'https://github.com/torvalds'
