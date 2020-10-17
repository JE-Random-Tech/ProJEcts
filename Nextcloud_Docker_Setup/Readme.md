# Netsuite Docker Setup (Using Postgres (DB) and Traefik (SSL) on QNAP NAS)

Have you wondered how to attach already existing data to Nextcloud, how to solve the painful permission issues and what to do if typical ports like 443 and 80 are already used by your NAS then this article is for you.

## Disclaimer

I am in no way a professional so everything is at your own risk. That said if you have improvements or problems feel free to open an issue or fork and create a pull request.

## Acknowledgement 

"TEAM – Together Everyone Achieves More". I want to thank the following people for theire help in creating and improving this article:

<!-- TODO-->

## Summary
 * existing data is mounted after creating USER to `/var/www/html/data/USER/files`
 * data is accessed using NFS and the option `ALL_SQUASH` to avoid permission issues
 * dyndns and port forwarding is used to nullify port issues
