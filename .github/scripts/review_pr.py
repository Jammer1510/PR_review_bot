import os
import requests
import openai
from github import Github

# Load Secrets from GitHub Actions
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_OWNER = "Jammer1510"  # Change this to your GitHub username/org
REPO_NAME = "PR_review_bot"  # Change this to your actual repository name

# OpenAI API Key Setup
openai.api_key = OPENAI_API_KEY
client = openai.Client()  # ✅ Use the new OpenAI client

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
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching PR diff: {response.text}")
        return ""

def analyze_code_with_openai(code_diff):
    """Send PR code diff to OpenAI GPT-4 Turbo for review."""
    if not code_diff.strip():
        return "No code changes detected in this PR."

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI reviewing code changes in a pull request."},
                {"role": "user", "content": f"Review the following GitHub Pull Request diff and provide code improvement suggestions:\n\n{code_diff}"}
            ],
            max_tokens=500  # Limit to 500 tokens to control cost
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

def post_review_comment(pr, review_comment):
    """Post review comments on GitHub PR."""
    try:
        pr.create_issue_comment(review_comment)
        print("Review comment posted successfully.")
    except Exception as e:
        print(f"Error posting review comment: {str(e)}")

def approve_pr(pr):
    """Approve PR if the review suggests it is good."""
    try:
        pr.create_review(event="APPROVE", body="LGTM! Approving this PR.")
        print("PR Approved!")
    except Exception as e:
        print(f"Error approving PR: {str(e)}")

def merge_pr(pr):
    """Auto-merge the PR if it meets criteria."""
    try:
        pr.merge(commit_message="Auto-merging reviewed PR.")
        print("PR Merged Successfully!")
    except Exception as e:
        print(f"Error merging PR: {str(e)}")

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

    review_comment = analyze_code_with_openai(code_diff)
    post_review_comment(pr, review_comment)

    # If AI review includes "LGTM", approve & merge the PR
    if "LGTM" in review_comment:
        approve_pr(pr)
        merge_pr(pr)

if __name__ == "__main__":
    main()
