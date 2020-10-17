# Netsuite Docker Setup (Using Postgres (DB) and Traefik (SSL) on QNAP NAS)

Have you wondered how to attach already existing data to Nextcloud, how to solve the painful permission issues and what to do if typical ports like 443 and 80 are already used by your NAS then this article is for you.

## Disclaimer

I am in no way a professional so everything is at your own risk. That said if you have improvements or problems feel free to open an issue or fork and create a pull request.

## Acknowledgement 

"TEAM – Together Everyone Achieves More". I want to thank the following people for theire help in creating and improving this article:
 * @t0bska
<!-- TODO-->

## Summary
 * existing data is mounted after creating USER to `/var/www/html/data/USER/files`
 * data is accessed using NFS and the option `ALL_SQUASH` to avoid permission issues
 * dyndns and port forwarding is used to nullify port issues

## Get Started
Docker in general is a versatile tool which is always good to know and be aware of the basic features like compose, network and volumes. [docker-curriculum](https://docker-curriculum.com/) is one of the best to get started.

## Infrastructure
First you need to set up a dynamic DNS. The idea is to update the ip-adress after every change. There are a lot of free options out there. As one of my friends suggested, I opted for [dnshome](https://www.dnshome.de/). Make sure that `YOUR@EMAIL.com` matches the one you use for your dynDNS. Then you can set up port forwarding. Chose the ip-adress of youre device and map the external port 80 to 8880 and 443 to 4433 respectively. It is very important to specify the external port to 80 and 443 and not to 8880 or  4433 because then the logs of traefik go wild and it tries for whatever reason a wrong resolver (tls-alpn-01) which coresponds to a DNS challenge instead of the specified HTTP challenge (http-01) and then failes to revoke the authentication. This definately did not happen to me and I did not waste a day figuring that one out ;-). A massive thanks to the reddit user [vividboarder](https://www.reddit.com/r/qnap/comments/cbt8o5/setup_for_traefik_or_other_reverse_proxies_on/).