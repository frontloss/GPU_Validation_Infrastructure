For the app to work, you need to create _netrc file.

1. Navigate To https://gta.intel.com
2. Click Drop Down Arrow on Your Name at the right corner of your browser
3. Select "My API Keys"
4. Click "Add an API Key". Provide Some Name and click "Generate"
5. A new key will be generated
6. Navigate to USER PROFILE e.g. C:\USERS\DPATIL and create a file named _netrc
7. Dump your API key inside _netrc file. File content will be like -

 machine gta.intel.com
    login <username-api>
    password <64bit password>

8. Save the file without any extension.

Once Done, open the app, Navigate to the required page, enter all the fields and click submit. 

Once the execution request is submitted, you will receive an EMAIL from WF Manager about GTA jobs which can be further monitored. 
WF Manager will sent a note after the execution has completed. 

Please see https://securewiki.ith.intel.com/display/GfxDisplay/EagleTon for additional infomration on usage and known resolutions for issues, if any. 