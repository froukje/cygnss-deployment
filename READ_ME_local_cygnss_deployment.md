## Working: Created a new branch demo for Demo at retreat. This code will run prefect tasks on local.  And, resulting data will be saved in database. Then, from updated database, data will be shown in streamlit dashboard to the user.


 
- Install mongo if not installed: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
- Open a terminal
  - Start MongoDB: sudo service mongo start
  - If mongo.service not found
    -   Most probably unit mongodb.service is masked. Use following command to unmask it: sudo `systemctl unmask mongod`
    -   and re-run: `sudo service mongod start`
    -   Verify that MongoDB has started successfully: `sudo service mongod status`
-   Activate conda environment: `conda activate <ENV_NAME>` or your conda 
-   Start Orion Server for seeing the UI: `prefect orion start`
     -   If you want to schedule via prefect, run these, else skip:
         -   Start a new terminal 
         -   Activate the conda env, `conda activate <ENV_NAME>`
         -   Run: `prefect agent start -q demo`
-   New terminal: 
     -   cd  `<navigate to Parent folder of cygnss-deployment> `
     -   Run:  python cygnss-deployment/prefect-deploy.py
     -   New terminal: mlflow ui 


	
