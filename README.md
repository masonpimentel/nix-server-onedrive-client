## Unix Server OneDrive Client


This application will allow you to automate uploading directories from a Unix-based server to your OneDrive cloud storage. The primary application of this is backup redundancy using your OneDrive service for critical directories such as a Git remote.

This README is more of a guide and includes instructions on everything from setting up your (microsoft project), to setting up the Python application and setting up the cron jobs on your server.

Note that this guide assumes you are using a Unix cron scheduler but theoretically you could run this from any machine as long as it has a scheduler and can run Python. In this case we would normally call this machine the 'server' but actually the way it's applied here it's more of a client as it will be interacting with (microsoft)

What you will need:
- A 24/7 running machine with a scheduler that can run Python
- Access to a Microsoft account for (setting up project)

The guide consists of the following:

- Using the (microsoft to set up project)
- Setting up the Python application that implements the logic required to utilize the above services
- Setting up the cronjobs that can be run on a Unix-based server to execute the Python application at a given interval

What you will need:
- A machine with a scheduler that can run Python - ideally with 24/7 availability
- Access to a Microsoft account for creating the application
- Access to the Microsoft account with OneDrive storage provisioned (this can be the same as the account used to create the application)

### Create Microsoft Application

In order to use Microsoft's services API which is referred to as Microsoft Graph, you will need to use your account to register an application. To do so, visit their application registration portal:

https://apps.dev.microsoft.com/

Once you've signed in, click on "Add an app". Give your app a name and click on "Create application".

![](documentation/screenshots/screen1.png) |
------------ | 
_Creating the Microsoft application_ |


First thing you want to do is generate a new application secret in password form. So click on "Generate New Password". Be sure to save the client secret! You'll eventually enter this in your configuration file.

![](documentation/screenshots/screen2.png) |
------------ | 
_Getting a client secret_ |

Next you're going to want to add your platform. We're going to authenticate in the browser so click on "Add Platform", then "Web"


![](documentation/screenshots/screen3.png) |
------------ | 
_Adding the web platform_ |

Add the following as the redirect URL: `http://localhost:8000/unix-server-onedrive-client/callback`. If you decide to go with something different you'd have to change the url in the config, see TODO section below.

![](documentation/screenshots/screen4.png) |
------------ | 
_Adding the redirect URL_ |

The default permissions work for the purposes of the app. Click on "Save" at the bottom to save your changes.

Before leaving, save your application ID.

![](documentation/screenshots/screen5.png) |
------------ | 
_Saving the application ID_ |

### Set up Python Application

#### Clone repository

Make sure you're in the directory where you want to run the Python application and Cronjob from. The rest of these steps will denote the current directory by `<path>`

```
$ git clone https://github.com/snxfz947/unix-server-onedrive-client.git
```

Alternatively, if you want to use SSH:

```
$ git clone git@github.com:snxfz947/unix-server-onedrive-client.git
```

#### Install relevant tools

To run the Python application you will need to install Python as well as some dependencies.

##### Python

The steps you take to install Python largely depends on the OS or distribution you're using. Chances are you already have Python installed or it was there by default. **The most important thing is that you have Python 3** (not Python 2). You will also need [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) for Python 3. Here are the steps for installing from the Python docs:

https://docs.python-guide.org/starting/install3/linux/

If you decided to go with Ubuntu 18.04 server, Python 3 is already installed but pip can be installed using the following:

```
$ sudo apt-get install python3-pip
``` 

Check your Python version using the `-V` argument:

```
$ python3 -V
Python 3.6.5
```

Note that for the particular Ubuntu server version `python3` is used to invoke Python 3, `python` runs Python 2. Similarly for pip, `pip3` is used to invoke the package manager for Python 3.

Check that `pip3` is set up correctly:

```
$ pip3 -V
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```

##### Dependencies

Run the following to install the necessary Python packages:

```
$ pip3 install filesplit requests
```

Run the following (on Ubuntu at least) to install jq:

```
$ sudo apt install jq
```

#### Complete configuration JSON

For running the app, the only configuration file that needs to be modified is the `user_config.json` file. `dev_config.json` contains all the configuration values that would be modified for development purposes only. 

ST

##### Required fields

client_id

client_secret

upload_pairs.local_dir
upload_pairs.server_dir

##### Optional/adjustable fields

##### Verbosity settings

#### Configure token

We will now use our credentials to get our API token for sending requests to our application.

Run the `config` script:

```
$ cd <path>/unix-server-onedrive-client
$ ./config
```

### Using the App

#### Running for the First Time

#### Viewing Logs

To see the logs, open `<path>/unix-server-onedrive-client/output.txt` This can be done by running:

```
$ cat <path>/unix-server-onedrive-client/output.txt
```

![](documentation/screenshots/screen18.png) |
------------ | 
_Viewing the logs_ |

Here you can see that the cronjob detected that the app was not running, so it started it up. This is indicated by the `CRONJOB:` tag. You can also see that `receive` has started, and `send` has sent it's first message.

#### Clearing Logs

To clear the logs, run:

```
$ cd <path>/unix-server-onedrive-client
$ ./clear
```

### Scheduling Runs Using Cron