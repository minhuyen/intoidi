The latest Mezzanine with Django configured to work on Redhat Openshift (http://openshift.redhat.com).

Copy you mezzanine project files under wsgi directory.

Under wsgi subfolder you can safely replace all files except:

 - application (runs the Mezzanine under the Apache web process)
 - rhcmanage.py (ala manage.py adjusted to fit the Openshift environment)
 - local_settings.py (adjusted to recognize local PC vs the Openshift environment and t)
 - debug_settings.py (for the convenience debug on/off switch on particular environment)

Other files are just stock Mezzanine project files.

rhc push the files into Openshift application.

ssh login to Openshift application and run:

   cd app-root/repo/wsgi
   python rhcmanage.py createdb (answer some questions provided)
   
See the result on your Openshift website.

__Advantages__

No changes needed for the local development. Use your manage.py on development PC as adviced by Mezzanine project.

No changes needed for the Openshift environment. local_settings.py are set in general to use the Openshift provided parameters.

__Full instructions for setup__

Create account on Redhat Openshift ( http://openshift.redhat.com ), install your rhc tools on local PC.

On local PC CD into the directory where you want to work with your application

    cd (my dir)

Create application and cd into the created dir (replace mezzanine with the name of your app)

    rhc app create mezzanine python-2.6 postgresql-9.2

Pull the adjustements

    cd mezzanine
    git remote add mezzanineopenshift -m master ssh://git@bitbucket.org:radeksvarz/mezzanineopenshift.git
    git pull -s recursive -X theirs mezzanineopenshift master
        
        
If you are on Windows, assure that the Openshift deployment hooks are executable

    git update-index --chmod=+x .openshift\action_hooks\build
    git update-index --chmod=+x .openshift\action_hooks\deploy

Optionaly adjust you requirements in the setup.py (do not forget to commit).
        
Push to openshift 

    git commit -m "initial mezzanine deploy"
    git push origin
    
SSH login to openshift application (replace mezzanine with the name of your app)

    rhc ssh mezzanine --ssh="c:\git\bin\ssh.exe" 
    cd app-root/repo/wsgi/
    python rhcmanage.py createdb
    
Check via browser your fresh Mezzanine installation :)
    
__Other info__

[![Requirements Status](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements.png?branch=master)](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements/?branch=master)

The OpenShift `python` cartridge documentation can be found at:

https://github.com/openshift/origin-server/tree/master/cartridges/openshift-origin-cartridge-python/README.md 
