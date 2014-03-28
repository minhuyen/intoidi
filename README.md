The latest Mezzanine with Django configured to work on Redhat Openshit (http://openshift.redhat.com).

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


__Other info__

[![Requirements Status](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements.png?branch=master)](https://requires.io/bitbucket/radeksvarz/mezzanineopenshift/requirements/?branch=master)

The OpenShift `python` cartridge documentation can be found at:

https://github.com/openshift/origin-server/tree/master/cartridges/openshift-origin-cartridge-python/README.md 
