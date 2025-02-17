import requests
import json

github_token = "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"
github_api_url = "https://api.github.com/graphql"

def get_user_repos(number_of_repos=3):
    headers = {"Authorization": f"Bearer {github_token}"}
    
    graphql_query = {
        "query": """
        query($number_of_repos:Int!) {
          viewer {
            name
            repositories(last: $number_of_repos) {
              nodes {
                name
                url
                stargazerCount
                description
                createdAt
                updatedAt
                primaryLanguage {
                  name
                }
                forkCount
                watchers {
                  totalCount
                }
                issues {
                  totalCount
                }
                pullRequests {
                  totalCount
                }
                licenseInfo {
                  name
                }
              }
            }
          }
        }
        """,
        "variables": {"number_of_repos": number_of_repos}
    }
    
    response = requests.post(github_api_url, headers=headers, json=graphql_query)
    
    if response.status_code == 200:
        data = response.json()
        repos = data.get("data", {}).get("viewer", {}).get("repositories", {}).get("nodes", [])
        
        for repo in repos:
            print(f"{repo.get('name')}: {repo.get('url')}")
            print(f"⭐ {repo.get('stargazerCount')} - {repo.get('description')}")
            print(f"🛠 Language: {repo.get('primaryLanguage', {}).get('name', 'N/A')}")
            print(f"🍴 Forks: {repo.get('forkCount')} | 👀 Watchers: {repo.get('watchers', {}).get('totalCount')}")
            print(f"🐛 Issues: {repo.get('issues', {}).get('totalCount')} | 🔀 PRs: {repo.get('pullRequests', {}).get('totalCount')}")
            print(f"📜 License: {repo.get('licenseInfo', {}).get('name', 'N/A')}")
            print(f"📅 Created: {repo.get('createdAt')} | 🔄 Updated: {repo.get('updatedAt')}")
            print("-" * 100)
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    get_user_repos(10)
