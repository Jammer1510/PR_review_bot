# 🚀 PR Review Bot - Automated Code Review Using GPT-4o


An AI-powered GitHub bot that automatically reviews Pull Requests (PRs) and commits using OpenAI's GPT-4o.✅ Provides improvement suggestions✅ Posts AI-generated comments on PRs & commits✅ Can auto-approve and merge PRs if they pass AI review


## 🛠️ Features

AI-Powered Code Review: Uses GPT-4o to analyze PRs and commits.

PR & Commit Support: Works on Pull Requests & direct commits.

GitHub Actions Integration: Automatically triggers on PRs and pushes to main or dev branches.

Auto-Approval & Merging: If AI review contains "LGTM", the bot approves & merges PRs.



## 📌 How It Works

A PR is opened, updated, or reopened → The bot fetches the code diff.

The bot sends the PR diff to GPT-4o for review.

GPT-4o analyzes the changes and provides feedback.

The bot posts a comment with AI-generated review suggestions.

If AI review contains "LGTM", the bot auto-approves & merges the PR.



## 📊 PR Review Statistics

| Review Status          | Count | Visual Representation |
|------------------------|------:|-----------------------|
| ✅ Approved           | 10    | ██████████            |
| ❌ Changes Requested | 5     | █████                 |
| 🔄 Pending           | 3     | ███                   |

📊 PR Review Summary

✅ Approved: ██████████ 10❌ Changes Requested: █████ 5🔄 Pending: ███ 3



## 🚀 Getting Started

1️⃣ Fork & Clone the Repository

```
git clone https://github.com/Jammer1510/PR_review_bot.git
cd PR_review_bot
```


2️⃣ Set Up Python Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```


3️⃣ Install Dependencies

`pip install -r requirements.txt`


4️⃣ Set Up GitHub Secrets

Go to GitHub → Repository Settings → Secrets and Variables → Actions, then add these secrets:

| Secret Name             | Description                                      | Required For |
|-------------------------|--------------------------------------------------|--------------|
| 🔑 `OPENAI_API_KEY`     | Your OpenAI API key (from [OpenAI API Keys](https://platform.openai.com/api-keys)) | AI Code Review |
| 🔑 `GITHUB_TOKEN`       | Available in GitHub Actions (no need to add manually) | Repository Access |
| 🔑 `PERSONAL_ACCESS_TOKEN` | GitHub token with `repo` and `write:discussion` permissions (Required for posting PR comments) | PR Comments |


## 🔧 Configuration

Modify .github/workflows/pr_review.yml to customize behavior:

on:
  pull_request:
    types: [opened, synchronize, reopened]
  push:
    branches:
      - main  # ✅ Runs on commits to `main`
      - dev   # ✅ Runs on commits to `dev`

Modify review_pr.py for AI review settings:
```
response = client.chat.completions.create(
    model="gpt-4o",  # ✅ Uses GPT-4o
    messages=[
        {"role": "system", "content": "You are an AI reviewing code changes in a PR."},
        {"role": "user", "content": f"Review this GitHub PR diff:\n\n{code_diff}"}
    ],
    max_tokens=200  # ✅ Controls response length
)
```


## 🧪 Testing Locally

You can manually trigger a review by setting environment variables:
```
export GITHUB_TOKEN="your-personal-access-token"
export OPENAI_API_KEY="your-openai-api-key"
export PR_NUMBER=1  # Replace with an actual PR number
python .github/scripts/review_pr.py
```


## 🚀 Deployment

Once set up, the bot runs automatically whenever a PR is created or code is pushed.

✅ Open a PR or push to main/dev → GitHub Actions runs the bot → AI review is posted!


## 📜 License

This project is open-source under the MIT License.

## 🙌 Contributors

Jammer1510 - Creator & Maintainer

