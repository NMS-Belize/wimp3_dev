Updating WIMP3 on Production Server
---------------------------------------------------------------------

STEP 1: Update Git Repository with the following commands:

git status
git add .
git commit -m "Description"
git push origin main

STEP 2: Open new terminal to connect to Production Server:
ssh wimp3@192.168.3.73
Enter password

Navigate to project directory
cd wimp3/wimp3_dev

STEP 3: Pull updated files from Git Repository
git pull

STEP 4: Create/Update Migrations
python3 manage.py migrate forecasts