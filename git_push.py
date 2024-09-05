from git import Repo, GitCommandError
import time
import os

def commit_changes(repo_directory, commit_message="Committing changes from script"):
    try:
        repo = Repo(repo_directory)
        
        # Fetch Git user details from environment variables
        git_author_name = os.getenv('GIT_AUTHOR_NAME')
        git_author_email = os.getenv('GIT_AUTHOR_EMAIL')
        git_committer_name = os.getenv('GIT_COMMITTER_NAME')  # Use author name if committer name is not set
        git_committer_email = os.getenv('GIT_COMMITTER_EMAIL')  # Use author email if committer email is not set

        # Check if required environment variables are set
        if not git_author_name or not git_author_email:
            raise ValueError("Git author name and email must be set via environment variables.")

        # Set the Git committer identity using environment variables
        with repo.config_writer() as config:
            config.set_value("user", "name", git_committer_name)
            config.set_value("user", "email", git_committer_email)

        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            print("Changes committed locally")
        else:
            print("No changes to commit.")
    
    except GitCommandError as e:
        print(f"An error occurred while committing: {e.stderr}")
    except ValueError as e:
        print(f"Error: {e}")

def push_changes(repo_directory, github_token, github_url, reconcile_strategy='ours', max_retries=5, delay=3):
    # Remove the protocol from the GitHub URL if present
    github_url_cleaned = github_url.replace("https://", "").replace("http://", "")

    # Set environment variables for Git authentication
    os.environ['GIT_ASKPASS'] = 'echo'
    os.environ['GIT_USERNAME'] = 'x-access-token'
    os.environ['GIT_PASSWORD'] = github_token

    attempt = 0
    while attempt < max_retries:
        try:
            repo = Repo(repo_directory)
            origin = repo.remote(name='origin')

            # Update the remote URL to use the token for authentication
            remote_url = f'https://{github_token}@{github_url_cleaned}'  # Correct URL format without duplicate protocol
            origin.set_url(remote_url)

            try:
                # Pull changes without auto-merging
                pull_info = origin.pull(strategy_option=None)
                print("Pulled latest changes from remote")
            except GitCommandError as e:
                if 'divergent branches' in e.stderr:
                    print("Detected divergent branches. Attempting to reconcile with strategy:", reconcile_strategy)
                    if reconcile_strategy == 'ours':
                        repo.git.merge('-X', 'ours')
                    elif reconcile_strategy == 'theirs':
                        repo.git.merge('-X', 'theirs')
                    else:
                        raise e
                else:
                    raise e

            # Push the changes to the remote repository
            origin.push()
            print("Changes pushed to the repository")
            return

        except GitCommandError as e:
            print(f"An error occurred while pushing: {e.stderr}")
            attempt += 1
            if attempt < max_retries:
                print(f"Retrying push... (Attempt {attempt}/{max_retries})")
                time.sleep(delay)
            else:
                print("Max retries reached. Push failed.")
