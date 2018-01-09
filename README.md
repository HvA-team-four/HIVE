<img src="https://hive.airsweeper.nl/branding/logo.png" width="250">
HIVE is a Dark Web Crawler created by FOUR on behalf of a large Dutch firm. Please note that the HIVE is a proof-of-concept and should not be used in a live-environment. 


### Install
HIVE and all of its prerequisites can easily be installed using the Install_HIVE.sh script located at the Deployment folder of the HIVE release. 

* Run ```sudo bash Install_HIVE.sh``` and accept the EULA.

### Start



* Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) if you haven't already.
* Run ```vagrant up```. Once it is online shut it down with ```vagrant halt```.
* Run ```vagrant box update```. This ensures you have to latest version of scotchbox.
* Run ```vagrant up```. This will start the virtual machine, first setup will take a while.
* Run ```vagrant ssh```. This way you'll get into the virtual machine.
* Run ```python3.6 crawler/main.py``` Just to see is everything is working correctly. 
* Test


