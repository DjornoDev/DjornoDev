import subprocess
import time
import random

def run_git_command(command):
    """Execute a git command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=r"d:\PERSONAL\MY PROJECTS\DjornoDev")
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def make_commit(commit_number):
    """Make a single commit by appending a comment to README.md"""
    
    # Read the current README
    readme_path = r"d:\PERSONAL\MY PROJECTS\DjornoDev\README.md"
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Append a comment at the end
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        new_content = content + f"\n<!-- Auto commit #{commit_number} - {timestamp} -->"
        
        # Write back to README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # Git add
        success, stdout, stderr = run_git_command("git add README.md")
        if not success:
            print(f"❌ Failed to add README.md: {stderr}")
            return False
        
        # Git commit
        commit_message = f"Auto commit #{commit_number}: Update README"
        success, stdout, stderr = run_git_command(f'git commit -m "{commit_message}"')
        if not success:
            print(f"❌ Failed to commit: {stderr}")
            return False
        
        print(f"✅ Commit #{commit_number} successful: {commit_message}")
        return True
        
    except Exception as e:
        print(f"❌ Error on commit #{commit_number}: {str(e)}")
        return False

def main():
    print("🚀 Starting automated commits...")
    print("=" * 50)
    
    # Check if we're in a git repository
    success, stdout, stderr = run_git_command("git status")
    if not success:
        print("❌ Not a git repository or git is not available")
        return
    
    successful_commits = 0
    failed_commits = 0
    
    # Make 30 commits
    for i in range(1, 31):
        print(f"\n📝 Creating commit {i}/30...")
        
        if make_commit(i):
            successful_commits += 1
        else:
            failed_commits += 1
        
        # Small delay between commits (0.5 to 1.5 seconds)
        if i < 30:
            delay = random.uniform(0.5, 1.5)
            time.sleep(delay)
    
    print("\n" + "=" * 50)
    print("🎉 Automated commits completed!")
    print(f"✅ Successful: {successful_commits}")
    print(f"❌ Failed: {failed_commits}")
    print("\n💡 Don't forget to push your commits:")
    print("   git push origin main")

if __name__ == "__main__":
    main()
