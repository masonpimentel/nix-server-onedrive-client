## Unix Server OneDrive Client


This application will allow you to upload and download directories to and from a Unix-based server. The primary application of this is backup redundancy using your OneDrive service. This would allow you to have a cloud backup of your server directories (such as a directory of Git repositories) and conversely an on-premise backup of your cloud directories.

This README is more of a guide and includes instructions on everything from setting up your (microsoft project), to setting up the Python application and setting up the cron jobs on your server.

Note that this guide assumes you are using a Unix cron scheduler but theoretically you could run this from any machine as long as it has a scheduler and can run Python. In this case we would normally call this machine the 'server' but actually the way it's applied here it's more of a client as it will be interacting with (microsoft)

What you will need:
- A 24/7 running machine with a scheduler that can run Python
- Access to a Microsoft account for (setting up project)

The guide consists of the following:

- Using the (microsoft to set up project)
- Setting up the Python application that implements the logic required to utilize the above services
- Setting up the cronjobs that can be run on a Unix-based server to execute the Python application at a given interval


### Create Microsoft Application

In order to use Microsoft's services API which is referred to as Microsoft Graph, you will need to use your Microsoft account to register an application. To do so, visit their application registration portal:

https://apps.dev.microsoft.com/

Once you've signed in, click on "Add an app". Give your app a name and click on "Create application".

Screen1
Creating the Microsoft application

First thing you want to do is generate a new application secret in password form. So click on "Generate New Password". Be sure to save the client secret! You'll eventually enter this in your configuration file.

Screen2
Getting a client secret

Next you're going to want to add your platform. We're going to authenticate in the browser so click on "Add Platform", then "Web"

Screen3
Adding the web platform

Add the following as the redirect URL: `http://localhost:8000/unix-server-onedrive-client/callback`. If you decide to go with something different you'd have to change the url in the config, see TODO section below.

Screen4
Adding the redirect URL

The default permissions work for the purposes of the app. Click on "Save" at the bottom to save your changes.

Before leaving, save your application ID.

Screen5
Saving the application ID