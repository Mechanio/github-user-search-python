import json
import requests
import graphene


class UserInfoQuery(graphene.ObjectType):
    """
    GitHub user info for schema
    """
    url = graphene.String()
    name = graphene.String()
    avatarUrl = graphene.String()
    htmlUrl = graphene.String()


class UserReposQuery(graphene.ObjectType):
    """
    GitHub user repositories for schema
    """
    repoName = graphene.String()
    repoHtmlUrl = graphene.String()


class Query(graphene.ObjectType):
    """
    Query for schema
    """
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
        if len(user_repos) == 0:
            return results
        for i in range(len(user_repos)):
            temp = UserReposQuery(repoName=user_repos[i]['name'],
                                  repoHtmlUrl=user_repos[i]['html_url'])
            results.append(temp)
        return results


schema = graphene.Schema(query=Query)
