import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(__file__))
packages = [
    os.path.join(ROOT, "packages", "actionformats"),
    os.path.join(ROOT, "packages", "elementals"),
]

def main():
    for pkg in packages:
        print(f"== Building {pkg} ==")
        subprocess.check_call([sys.executable, "-m", "build"], cwd=pkg)
    print("All builds completed.")

if __name__ == "__main__":
    main()
