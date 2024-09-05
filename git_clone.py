import os
import shutil
import stat
import pygit2

#def handle_remove_readonly(func, path, exc_info):
#    """
#    Handle the read-only file removal.
#    """
#    os.chmod(path, stat.S_IWRITE)
#    func(path)

def clone_repo(github_token):
    """
    Clones the repository using the provided GitHub token and URL from the environment variable.
    """
    # Fetch the GitHub URL from environment variables
    repo_url = os.getenv("GITHUB_URL")
    if not repo_url:
        raise ValueError("GITHUB_URL environment variable is not set.")
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    repo_name = os.path.basename(repo_url).replace('.git', '')
    clone_directory = os.path.join(current_directory, repo_name)

    #if os.path.exists(clone_directory):
    #    print(f"Directory {clone_directory} already exists. Deleting it.")
    #    shutil.rmtree(clone_directory, onerror=handle_remove_readonly)
    #    print(f"Deleted {clone_directory}")

    try:
        # Use pygit2 credentials for cloning
        credentials = pygit2.UserPass(github_token, "x-oauth-basic")
        pygit2.clone_repository(repo_url, clone_directory, callbacks=pygit2.RemoteCallbacks(credentials=credentials))
        print(f"Repository cloned into {clone_directory}")
    except Exception as e:
        print(f"An error occurred: {e}")
