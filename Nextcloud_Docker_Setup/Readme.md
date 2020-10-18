# Netsuite Docker Setup (Using Postgres (DB) and Traefik (SSL) on QNAP NAS)

Have you wondered how to attach already existing data to Nextcloud, how to solve the painful permission issues and what to do if typical ports like 443 and 80 are already used by your NAS then this article is for you.

## Disclaimer

I am in no way a professional so everything is at your own risk. That said if you have improvements or problems feel free to open an issue or fork and create a pull request.

## Acknowledgement 

"TEAM – Together Everyone Achieves More". I want to thank the following people for theire help in creating and improving this article:
 * [@t0bska](https://github.com/t0bska)
<!-- TODO-->

## Summary
 * dyndns and port forwarding is used to nullify port issues
 * data is accessed using NFS and the option `ALL_SQUASH` to avoid permission issues
 * existing data is mounted after creating USER to `/var/www/html/data/USER/files`


## Get Started
Docker in general is a versatile tool which is always good to know and be aware of the basic features like compose, network and volumes. [docker-curriculum](https://docker-curriculum.com/) is one of the best to get started. To clone this subfolder you can either use `git clone https://github.com/JE-Random-Tech/ProJEcts.git` and remove the other folders or install snv using `sudo apt install subversion` followed by `svn checkout https://github.com/JE-Random-Tech/ProJEcts/trunk/Nextcloud_Docker_Setup` to copy this subfolder. More about that [here](https://stackoverflow.com/questions/7106012/download-a-single-folder-or-directory-from-a-github-repo). Before we start the conatiners we have to set up our infrastructure and specify certain parts of the docker-compose.yaml file. (QNAP enable ssh and use e.g. putty or Container Station -> create -> create application (button))

## Setup
### DynDNS and port forwarding
First you need to set up a dynamic DNS. The idea is that for example the router after every ip adress change sends its new one to the service. There are a lot of free options out there. As one of my friends suggested, I opted for [dnshome](https://www.dnshome.de/). Make sure that `YOUR@EMAIL.com` matches the one you use for your dynDNS and specify `YOUR.DOMAIN.com` (!make sure to adapt the one in the nextcoud section as well). Then you can set up port forwarding. Chose the ip-adress of youre device and map the external port 80 to 8880 and 443 to 4433 respectively. It is very important to specify the external port to 80 and 443 and not to 8880 or  4433 because then the logs of traefik go wild and it tries for whatever reason a wrong resolver (tls-alpn-01) which coresponds to a DNS challenge instead of the specified HTTP challenge (http-01) and then failes to revoke the authentication. This definitely did not happen to me and I did not waste a day figuring that one out ;-). A massive thanks to the reddit user [vividboarder](https://www.reddit.com/r/qnap/comments/cbt8o5/setup_for_traefik_or_other_reverse_proxies_on/) for the hint and [@ismailyenigul](https://github.com/ismailyenigul) for providing the [traefik labels](https://github.com/nextcloud/docker/issues/1061). (FritzBox: Internet -> Permit Access -> Port sharing / DynDNS)

###  NFS
After that we have to configure the Network File System (NFS). Before we do that though I want to explain why we can't simply mount the file location to docker. Nextcloud uses www-data to read and write. The user has a User ID (UID) and Group ID (GID) of 33. Then, as docker just passes UID and GID, with `setfacl` we could add a permission for specific ID's lile 33. However it is not enough to grand read write access as Nextcloud still has permission issues it also requires the execute permission. If you grant this Permission as well Nextcloud, at least on my test VM, locks the folder and root rights are required to access the data. A way around this problem is to specify the user in the docker-compose file. Be aware that you also have to change permissions to the exposed files to the specified user. This is not enough though if there is more than one user and folders with different permissions set. 

With NFS we can specify for every shared folder the "mappping" of the user. With the option `ALL_SQUASH` www-data is set to a specified user. Pease set the allowed IP-Adress to the one from the device hosting the Nextcloud/Docker service.  Please configure `IPADRESSOFNFSSERVICE` and `/PATH/TO/STORAGE`. Repeat for multiple shared folders. Make sure to name the volume differently and mount it to the nextcloud service as `foldername` in the example (QNAP: Control Center -> Shared Folders -> Edit shared folder Permission (small icon in action column) -> NFS host access (dropdown)):

The NFS Solution is just a workaround though. If you for example have a family folder every Nextcloud account is squashed to the same account. Here the GID is important and the fact that the folder is accessible by the group. Then every user part of the group has read write access solely the owner is not properly set. In a perfect world Nextcloud would have the option to map every user to an existing one on the host system (If you found another way please open an issue).

### Mount existing data
Now we have to specify user and password as well as the name of the database service postgres. Please adapt `DATABASENAME`, `DATABASEUSER` and `DATABASEPASSWORD` in the postgres AND the nextcloud section. Then using `docker-compose up` we can start the containers. If everything worked correctly you can access Nextcloud in a browser using `YOUR.DOMAIN.com` and start specifying the admin user name and password (If you have problems I encourage you to open an issue). Then you can activate the app external storage and in settings add a local storage with the path `/external/media`. A green checkmark should appear next to the setting (check your NFS settings if you have problems). Go back to the files tap and validate that new files can be created.
To mount the data properly remove the external storage setting and specify the target of the volume in the nextcloud service to `/var/www/html/data/USER/files` where USER is the user you want to mount the files to. Restart the container and use `docker exec --user www-data nextcloud php occ files:scan --all`. Log into nextcloud and go to the files tap. You should see the content of `/PATH/TO/STORAGE`. To always scan for external changes if you for example mounted your files to the windows explorer add `'filesystem_check_changes' => 1,` to the config.php file located in the nextcloudconfigurationdata folder relative to the docker-compose.yml file.

## Conclusion
I hope this article helped you setting up Nextcloud. If you want to see more tutorials or proJEcts like this take a look at my [YouTube](https://www.youtube.com/channel/UCon2LqPY3CJUGIAhMsOnpIA) channel. Have a nice day.

## Debug and common issues
This section contains tips and tricks as well as common issues because let's face it you most likely ran into one. First of all please go over the docker-compose.yaml file and make sure that all parameters are properly set (all of them are at the beginning in capital letters).
### QNAP
If you have problems to start the containers ssh into your NAS using e.g. putty and cd to the directory containing the compose file (mostly starts with `/share/PATH/TODIRECTORY`). Then you can execute `docker-compose up` and get the error message.
### Docker
To get access to the terminals of your containers use `docker exec -it CONTAINERNAME bash` where CONTAINERNAME is either nextcloud, postgres or traefik. You can also expose certain ports. If you want to check if your nextcloud container is accessible expose port 80. You can map it like the example shows in the traefik service with `ports: - YOURPORT:80`. 