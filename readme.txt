Updating WIMP3 on Production Server
---------------------------------------------------------------------

STEP 1: Update Git repository with the following commands:

git status
git add .
git commit -m "Description"


STEP 2: Open new terminal to connect to Production Server:
ssh wimp3@192.168.3.73
Enter password

Navigate to project directory
cd wimp3/wimp3_dev

Pull updated files from Git Repository
git pull

python3 manage.py migrate forecasts