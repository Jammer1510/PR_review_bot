import os
import requests
from github import Github

# Load Secrets
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
REPO_OWNER = "Jammer1510"  # Replace with your GitHub username/org
REPO_NAME = "PR_review_bot"  # Replace with your actual repo name
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Initialize GitHub Client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

def fetch_pr_details(pr_number):
    """Fetch PR details from GitHub."""
    pr = repo.get_pull(pr_number)
    return pr

def fetch_pr_diff(pr):
    """Get PR diff as text."""
    response = requests.get(pr.diff_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    return response.text if response.status_code == 200 else ""

def analyze_code_with_deepseek(code_diff):
    """Send PR code diff to DeepSeek for review."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "deepseek-coder",
        "messages": [
            {"role": "system", "content": "You are an AI reviewing code changes in a pull request."},
            {"role": "user", "content": f"Review the following GitHub Pull Request diff and provide code improvement suggestions:\n\n{code_diff}"}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error from DeepSeek API: {response.text}"

def post_review_comment(pr, review_comment):
    """Post review comments on GitHub PR."""
    pr.create_issue_comment(review_comment)

def approve_pr(pr):
    """Approve PR if it meets criteria."""
    pr.create_review(event="APPROVE", body="Looks good! Approving this PR.")

def merge_pr(pr):
    """Auto-merge the PR if it meets criteria."""
    pr.merge(commit_message="Auto-merging reviewed PR.")

def main():
    """Main function to process PRs."""
    pr_number = int(os.getenv("PR_NUMBER", 0))
    if pr_number == 0:
        print("No PR number provided. Exiting.")
        return
    
    pr = fetch_pr_details(pr_number)
    code_diff = fetch_pr_diff(pr)
    
    if not code_diff:
        print("Failed to fetch PR diff.")
        return

    review_comment = analyze_code_with_deepseek(code_diff)
    post_review_comment(pr, review_comment)

    if "LGTM" in review_comment:  # Example: Auto-approve if AI says "LGTM"
        approve_pr(pr)
        merge_pr(pr)

if __name__ == "__main__":
    main()

# Testing PR Review Bot with OpenAI API (1)
