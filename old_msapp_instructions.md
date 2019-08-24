These are the old instructions using Microsoft's old app registration portal - set to be removed in September 2019

### Create Microsoft Application

In order to use Microsoft's services API which is referred to as Microsoft Graph, you will need to use your account to register an application. To do so, visit their application registration portal:

https://apps.dev.microsoft.com/

Once you've signed in, click on "Add an app". Give your app a name and click on "Create application".

![](documentation/screenshots/screen1.png) |
------------ | 
_Creating the Microsoft application_ |


First thing you want to do is generate a new application secret in password form. So click on "Generate New Password". Be sure to save the client secret! You'll eventually enter this in your configuration file as the `client_secret`.

![](documentation/screenshots/screen2.png) |
------------ | 
_Getting a client secret_ |

Next you're going to want to add your platform. We're going to authenticate in the browser so click on "Add Platform", then "Web".


![](documentation/screenshots/screen3.png) |
------------ | 
_Adding the web platform_ |

Add the following as the redirect URL: `http://localhost:8000/unix-server-onedrive-client/callback`.

![](documentation/screenshots/screen4.png) |
------------ | 
_Adding the redirect URL_ |

The default permissions work for the purposes of the app. Click on "Save" at the bottom to save your changes.

Before leaving, save your application ID. You'll enter this in the configuration file as the `client_id`.

![](documentation/screenshots/screen5.png) |
------------ | 
_Saving the application ID_ |