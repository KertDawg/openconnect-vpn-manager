# openconnect-vpn-manager
Manages certificates in OpenConnect VPN

OpenConnect VPN can use certificate authentication.  This program manages those certificates as well as the certificate authority (CA) that signs those certificates.

##  Installation and startup
This section assumes the use of Ubuntu 23 or 24 for the VPN server.

1. Install Python 3 and curses on the server.  The Ubuntu package for curses is `libncurses-dev` at this time.
1. Install OpenConnect VPN on your server.  We assume that the configuration is in `/etc/ocserv`.  If it's in a different folder, just change the example commands to fit your setup.
1. We assume that the ocserv.conf is set up to use the CA and CRL files in `/etc/ocserv/ssl` in the files `ca-cert.cfg`, `ca-cert.pem`, `ca-privkey.pem`, `client-cert.cfg`, `crl.tmpl`, and `crl.pem`.
1. Clone this repository somewhere on that server.  It can be anywhere.
1. Execute the script as a user that can read from and write to your /etc/ocserv directory.  This is important; you can't modify certificates if you can't write there!  As an example, run the script as `sudo ./openconnect-vpn-manager.py`


##  Create a CA
The first thing to be done is to generate a certificate authority.  Choose `Create certificate authority` from the main menu.  That's it.


##  Add a profile
A "profile" is once certificate that is authorized to connect to the VPN.  This can be a user, a device, or both.

1. Choose `Add a profile` from the main menu
1. Type the profile name.  This could be something like the user name or the device name.  Enter an empty string to cancel.
1. There will be a file in the `/etc/ocserv/ssl/profiles` folder with a `.p12` extension for that profile.  That is the certificate that you should use on the VPN client.
1. Leave the certificate files in the `profiles` folder.  This will allow this program to rekove those certificates later.  If you delete them, then if the system gets compromised, you can't revoke only some certificates.  You'll have to start over from the beginning of the VPN setup.


##  Remove a profile
This will remove the certificate from the list available to this program.  It will also add the offending certificate to the certificate revokation list (CRL) that the VPN server knows about.  This makes the server reject that certificate even though it's otherwise valid.

1. Choose `Remove a profile` from the main menu.
1. Press the number key associated with the profile you want to remove.
1. Press `y` to continue.
1. This program should send the VPN server process a signal to refresh the CRL in memory.  If this signal doesn't work for some reason, you can restart the `ocserv` service or process to do the same thing.  You could also wait for the time specified in the configuration files for the server process to refresh the CRL on its own.  Your choice depends on the severity of the problem.  If a client may be currently connected to the VPN, then a restart of the VPN service might be best to disconnect them.
