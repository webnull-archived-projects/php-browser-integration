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
        webserver.run()