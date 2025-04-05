# GIT GUIDELINES

## Branch types  
- `feature/`: new functionality (e.g., `feature/read_time`).  
- `fix/`: gug fixes (e.g., `fix/comments`).  
- `docs/`: documentation updates (e.g., `docs/readme`).  

## Standard workflow

### 1. Clone the repository

```sh 
  git clone git@github.com:{user}/{repo}.git
```
### 2. Sync with <code>main</code> branch

```sh 
  git checkout main
```
```sh
  git pull origin main
```
### 3. Create a new branch (`type/name`)
```sh 
  git checkout -b type/branch_name   # e.g., feature/read_time
```

### 4. Commit changes
```sh 
  git add .
```
```sh
  git commit -m "type: description"  # e.g.,"feature: read time added"
```

### 5. Push to remote
```sh 
    git push -u origin type/branch_name
``` 

## Undo operations
#### Undo last commit (keep changes staged)
```sh 
  git reset --soft HEAD~1
```

#### Undo last commit (unstage changes)
```sh
  git reset HEAD~1
``` 

#### Undo last commit (discard all changes)
```sh 
  git reset --hard HEAD~1
``` 

## PR Guidelines
   - Target branch: <code>main</code>
   - Title format: `type: description` (e.g., `feature: add read time`).
   - Description: include summary and testing.
   - Reviewers: assign at least 1. 
   - Merge branch after review approval.

### Update open PRs (after merging other PRs)
If <code>main</code> has been updated, after merging another PR,
rebase the open PR branch to avoid conflicts before merging.
```sh
  # 1. Sync local main branch with remote
  git checkout main && git pull origin main
  # 2. Rebase PR branch onto the updated main (resolve conflicts)
  git checkout type/branch_name && git rebase main
  # 3. Push PR branch to remote
  git push origin type/branch_name
``` 

## After merge
#### Sync local <code>main</code> branch with remote
```sh 
  git checkout main
```
```sh
  git pull origin main
```
#### Optional cleanup: delete local merged branch
```sh
  git branch -d type/branch_name
```
