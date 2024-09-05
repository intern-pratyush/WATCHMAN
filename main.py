import git_clone
import change_yml
import git_push
import argparse
import os

def run_all(scale_type):
    # Fetch the GitHub token and URL from environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    github_url = os.getenv("GITHUB_URL")
    
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set.")
    
    if not github_url:
        raise ValueError("GITHUB_URL environment variable is not set.")

    # Cloning the repository
    print("Cloning the repository...")
    git_clone.clone_repo(github_token)

    # Running the change_yml file with the scale type from our end
    print(f"Modifying YAML files with scale type: {scale_type}")
    change_yml.main(scale_type)

    repo_path = r'/app/WATCHMAN'
    
    print("Committing changes...")
    git_push.commit_changes(repo_path)

    # Pushing changes to the repository
    print("Pushing changes to the repository...")
    git_push.push_changes(repo_path, github_token, github_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all scripts sequentially with a specified scale type.")
    parser.add_argument("--scale-type", choices=["scale_up", "scale_down"], required=True,
                        help="Specify whether to scale up or scale down replicas.")
    args = parser.parse_args()

    run_all(args.scale_type)
