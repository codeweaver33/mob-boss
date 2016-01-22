mob-boss
========

mob-boss is a rule management tool for Surricata expecially in clustered environments. It is used to pull down rules from a designated source (such as ET Pro) and parse them for use by Suricata IDS. mob-boss uses a configuration file (mob-boss.yaml) to set run options such as categories, github urls, and rule urls. mob-boss leverages github as its version control system. mob-boss also comes with rule_state.conf file which is a human readable file used for easily disabling/enabling sets of rules.

mob-boss can be used in clustered environments in combination with cron and git to keep rules synced across sensors. You can have a management host run mob-boss and then have the sensors periodically perform git pulls to pull down any changes to the rules that have come off of the management host.

For those who are wondering about the name: A suricata is another name for a meerkat, and a group of meerkats is called a mob. Hence the name mob-boss.

Installation
------------
mob-boss requires the use of Python3 in order to work properly. I recommend using pip3 as the package manager for the extras such as requests and PyYaml.

You can install the python module dependencies manually by installing the versions listed in [requirements.txt](requirements.txt) or automatically by running:
``` bash
$ pip3 install -r requirements.txt
```

Setup
-------

1) Clone this repository onto the target machine that will be running it.


2) Create a github repo that will be used for version control tracking of the rule changes. You will also use this git repo to make edits to the rule_state.conf file. Clone this repo onto the same machine(s) that will be running mob-boss in the loaction of your choosing. This repo will be where the all.rules file will be output by mob-boss.

3) Create a tmp dir that mob-boss will use as scratch space. It is recommended that you create this in /var/tmp/[somedir]. You will want this directory to persist across reboots.

4) Configure the mob-boss.yaml file with the appropriate configurations for your organization. You will need to provide the github urls that will be used by mob-boss for the CVS tracking of the rules. You will also need to enable/disable the categories that you wish for suricata to use. Also provide the url to the rules download location, and the temp-dir that you created in step 3.


Usage
-----
``` bash
$ python3 mob-boss.py -c [Location of mob-boss.yaml]
```

rule_state.conf
-----
This file which will be located in your output git directory is the file that you leverage to enable/disable rules. mob-boss automatically tracks when a rule is enabled/disabled by ETPro and will adjust the rule_state.conf accordingly. If a rule is removed by ETPro it will be removed in the rule_state.conf as well. Any new rule added by ETPro will show up in this file automatically. 
NOTE: Any rule that you disable will take precendence over ETPro. Any rule that ETPro disables will take precedence over you enabling it. 
NOTE (flowbits): mob-boss assumes that you are paying attention to flow bits. If you disable a rule that is in a flow bit chain, mob-boss will happily turn off that rule without looking for rules that might depend on it. 

A typical line in rule_state.conf:
````
sid,state,name
2404000,0,ET CNC Shadowserver Reported CnC Server IP group 1
````
To disable/enable a rule simply look for the sid in the file and then change the 0 -> 1 to enable or 1 -> 0 to disable. Re-run mob-boss to have the changes reflected in the all.rules file.

Reports
-----
Reports will be located in the report.md file in the git directory that you created. It will show any rules that were added in the last run, any rules that were removed, and any that were modified. This is designed to give a human readable report. To see specific diffs you can use git's commit diff functionality.


