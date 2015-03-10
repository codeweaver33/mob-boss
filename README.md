mob-boss
========

mob-boss is a rule management tool for Surricata. It is used to pull down rules from a designated source (such as ET Pro) and parse them for use by Suricata IDS. mob-boss uses a configuration file (mob-boss.yaml) to set run options such as categories, github urls, and rule urls. mob-boss leverages github as its CVS. mob-boss also comes with rule_state.conf file which is a human readable file used for easily disabling sets of rules.

For those who are wondering about the name: A suricata is another name for a meerkat, and a group of meerkats is called a mob. Hence the name mob-boss.

Installation
------------

You can install the python module dependencies manually by installing the versions listed in [requirements.txt](requirements.txt) or automatically by running:
``` bash
$ pip3 install -r requirements.txt
```

Setup
-------

1) Clone this repository onto the target machine that will be running it.

2) Create a github repo that will be used for CVS tracking of the rule changes. You will also use this git repo to make edits to the rule_state.conf file. Clone this repo onto the same machine that will be running mob-boss in the loaction of your choosing. This repo will be where the all.rules file will be output by mob-boss.

3) Create a tmp dir that mob-boss will use as scratch space. It is recommended that you create this in /var/tmp/[somedir]

4) Configure the mob-boss.yaml file with the appropriate configurations for your organization. You will need to provide the github urls that will be used by mob-boss for the CVS tracking of the rules. You will also need to enable/disable the categories that you wish for suricata to use. Also provide the url to the rules download location, and the temp-dir that you created in step 3.

5) When you run mob-boss for the first time the rule_state.conf file will be created, but it will not be populated correctly. You will need to run generateRuleState.py providing it with the path to the all.rules file as well as where you want the rule\_state.conf file to be output. This will create a properly formatted and fully populated rule_state.conf file.

Usage
-----
``` bash
$ python3 mob-boss.py -c [Location of mob-boss.yaml]
```
