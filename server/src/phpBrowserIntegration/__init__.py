#-*- encoding: utf-8 -*-
import pantheradesktop.kernel
import webserver
import args

def runInstance():
    """ Run instance of application """

    kernel = application()
    kernel.appName = 'php-browser-integration'
    kernel.coreClasses['gui'] = False
    kernel.coreClasses['db'] = False
    kernel.coreClasses['argsparsing'] = args.arguments
    kernel.initialize(quiet=True)
    kernel.hooking.addOption('app.mainloop', kernel.mainLoop)
    kernel.main()

class application (pantheradesktop.kernel.pantheraDesktopApplication, pantheradesktop.kernel.Singleton):
    """ Main class """

    def mainLoop(self, a=''):
        ## Set default configuration if it does not exists yet
        self.config.getKey('project.directories', [
            '/var/www/',
            '/srv/http/'
        ])
        self.config.getKey('ide.openFileCommand', '/usr/bin/kate %path% --line %line%')
        self.config.getKey('allowedHosts', ['localhost', '::1', '127.0.0.1'])

        webserver.run()