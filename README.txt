## Running StudyBuddy

1. Create a Firebase project and enable Firestore.
2. In Firebase Console → Settings → Service Accounts, click "Generate New Private Key".
3. Download the `.json` file.

4. Set the environment variable to point to that file:

   macOS/Linux:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/full/path/serviceAccount.json"

   -Run this command in your enviroment terminal

This is VERY important, as it wont run without this