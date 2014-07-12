#MezzanineOpenshift#

The latest Mezzanine with Django configured to work on Redhat Openshift (http://openshift.redhat.com).

Includes the convenient backup cron script for DB and media files.

Additionaly includes wwwroot with favicon.ico and robots.txt for adjustement.

[![Requirements Status](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements.png?branch=master)](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements/?branch=master)

##Quick info##

The concept is to merge 3 sources together:

  1. openshift python application project files
  2. adjustements from this repo (incl. Mezzanine template project files)
  3. your creations within Mezzanine project

The principles:

 - minimum adjustements needed
 - being able to run the application on local dev PC and server environment without file juggling
 - change behaviour via environment variables (e.g. DEBUG)

__Advantages__

No changes needed for the local development. Use your manage.py on development PC as adviced by Mezzanine project.

No changes needed for the Openshift environment. The file local_settings.py is set in general to use the Openshift provided parameters.

Backups daily with files retention. I.e. daily backups are stored 14 days, weekly 60 days, monthly 300 days. Other backups are deleted in order to preserve the storage.


##Quick intro for Openshift people##
  
(full instructions bellow)
  
  1. Copy you mezzanine project files under wsgi directory.

  2. Adjust your custom Django / Mezzanine settings in the #project_override_settings.py#

  3. and git push or sftp your changes to Openshift.

Under wsgi subfolder these files are crucial for the Mezzanine working on the Openshift:

 - application (runs the Mezzanine under the Apache web process)
 - local_settings.py (adjusted to recognize local PC vs the Openshift environment)
 - project_override_settings.py (your own settings)

Under wsgi/wwwroot subfolder you can safely replace all files.
 
Other files are just stock Mezzanine project files.

Backup feature requires cron cartridge.

##Debugging##

DEBUG settings are impplicitly False when deployed on Openshift and True on local PC development (auto setup).
Additionaly it is controlled by the environment variable DJANGO_DEBUG.

Set it on Openshift:

 - via ssh@openshift:  export DJANGO_DEBUG=True

 - or using rhc from local PC: rhc env-set DJANGO_DEBUG=True --app <appname>

__Full instructions for setup__

Create new account on Redhat Openshift ( http://openshift.redhat.com ), install your rhc tools on local PC (follow the instructions on the Openshift website).

On local PC CD into the directory where you want to work with your application

    cd (my dir)

Create application and cd into the created dir (replace mezzanine with the name of your app)

    rhc app create mezzanine python-2.7 postgresql-9.2 cron-1.4
    cd mezzanine
    
Delete not needed or conflicting files
    
    del * 
    
Pull the adjustements

    git remote add mezzanineopenshift -m master git@bitbucket.org:radeksvarz/mezzanineopenshift.git
    git pull -s recursive -X theirs mezzanineopenshift master
        
        
If you are on Windows, check and assure that the Openshift deployment hooks and backup scripts are executable

    git ls-tree master .openshift/action_hooks/
    git ls-tree master .openshift/cron/daily/

This should show 100755 at the beginning of build, deploy and backup.sh files, if not fix it:
    
    git update-index --chmod=+x .openshift\action_hooks\build
    git update-index --chmod=+x .openshift\action_hooks\deploy
    git update-index --chmod=+x .openshift\cron\daily\backup.sh

Optionaly adjust you dependencies in the setup.py.

Commit changes

    git add -A
    git commit -m "initial mezzanine deploy"
    
Push to openshift 

    git push origin
    
Now you can wait for a while for all dependencies to be downloaded on Openshift's server. It might report some warnings.
    
SSH login to openshift application (replace mezzanine with the name of your app)

    rhc ssh mezzanine --ssh="c:\git\bin\ssh.exe" 
    cd app-root/repo/wsgi/
    python manage.py createdb
    python manage.py migrate
    
Check via browser your fresh Mezzanine installation :)
    
__Other info__

The OpenShift `python` cartridge documentation can be found at:

https://github.com/openshift/origin-server/tree/master/cartridges/openshift-origin-cartridge-python/README.md 

Cron cartridge documentation

http://openshift.github.io/documentation/oo_cartridge_guide.html#cron

Special setup

Apache Status Page

Put the empty file named enable_public_server_statusmarker in your .openshift/markers/ directory to enable the Apache status page at URI /server-status
