from github import Github
from dotenv import dotenv_values
config = dotenv_values(".env")

def push_to_gh(token, filepath, plotname) -> True:

    g = Github(token)
    repo = g.get_user().get_repo('tw_feeds')
    git_filename = 'images/' + plotname
    images = repo.get_contents('images')

    with open(filepath, 'rb') as file:
        content = file.read()
        # Upload to github
        try:
            contents = repo.get_contents(git_filename)
            print(contents)
            repo.update_file(git_filename, "committing files", content, contents.sha, branch="main")
            print(git_filename + ' UPDATED')
        except:
            repo.create_file(git_filename, "committing files", content, branch="main")
            print(git_filename + ' CREATED')
    
    return True

push_to_gh(config['GHTOKEN'], 'dataplots/words.png', 'words.png')