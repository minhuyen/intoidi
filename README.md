#MezzanineOpenshift#

The latest Mezzanine with Django configured to work on Redhat Openshift (http://openshift.redhat.com).

Includes the convenient backup cron script for DB and media files.

[![Requirements Status](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements.png?branch=master)](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements/?branch=master)

##Quick info##

The concept is to merge 3 sources together:

  1. openshift python application project files
  2. adjustements from this repo (incl. Mezzanine template project files)
  3. your creations within Mezzanine project

The principles:

 - minimum adjustements needed
 - being able to run the application on local dev PC and life environment without file juggling
  
##Quick intro##
  
(full instructions bellow)
  
Copy you mezzanine project files under wsgi directory and git push or sftp your changes to Openshift.

Under wsgi subfolder you can safely replace all files except:

 - application (runs the Mezzanine under the Apache web process)
 - rhcmanage.py (ala manage.py adjusted to fit the Openshift environment)
 - local_settings.py (adjusted to recognize local PC vs the Openshift environment and t)
 - debug_settings.py (for the convenience debug on/off switch on particular environment)

Other files are just stock Mezzanine project files.

Backup feature requires cron cartridge.

__Advantages__

No changes needed for the local development. Use your manage.py on development PC as adviced by Mezzanine project.

No changes needed for the Openshift environment. local_settings.py are set in general to use the Openshift provided parameters.

Backups daily with files retention. I.e. daily backups are stored 14 days, weekly 60 days, monthly 300 days. Other backups are deleted in order to preserve the storage.

__Full instructions for setup__

Create account on Redhat Openshift ( http://openshift.redhat.com ), install your rhc tools on local PC.

On local PC CD into the directory where you want to work with your application

    cd (my dir)

Create application and cd into the created dir (replace mezzanine with the name of your app)

    rhc app create mezzanine python-2.6 postgresql-9.2 cron-1.4
    cd mezzanine
    
Delete not needed or conflicting files
    
    del * 
    
Pull the adjustements

    git remote add mezzanineopenshift -m master git@bitbucket.org:radeksvarz/mezzanineopenshift.git
    git pull -s recursive -X theirs mezzanineopenshift master
        
        
If you are on Windows, assure that the Openshift deployment hooks and backup scripts are executable

    git update-index --chmod=+x .openshift\action_hooks\build
    git update-index --chmod=+x .openshift\action_hooks\deploy
    git update-index --chmod=+x .openshift\cron\daily\backup.sh

Optionaly adjust you dependencies in the setup.py.

Commit changes

    git add -A
    git commit -m "initial mezzanine deploy"
    
Push to openshift 

    git push origin
    
Now you can wait for a while for all dependencies to be downloaded on Openshift app. It might through some warnings.
    
SSH login to openshift application (replace mezzanine with the name of your app)

    rhc ssh mezzanine --ssh="c:\git\bin\ssh.exe" 
    cd app-root/repo/wsgi/
    python rhcmanage.py createdb
    
Check via browser your fresh Mezzanine installation :)
    
__Other info__

The OpenShift `python` cartridge documentation can be found at:

https://github.com/openshift/origin-server/tree/master/cartridges/openshift-origin-cartridge-python/README.md 
