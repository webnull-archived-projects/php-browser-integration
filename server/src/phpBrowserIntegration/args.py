import pantheradesktop.kernel
import os
import subprocess
import sys

class arguments (pantheradesktop.argsparsing.pantheraArgsParsing):
    description = 'A simple bridge between Javascript and PHP/git that allows switching branch from web browser, or opening a file in favorite IDE with a click'

    def detectEditors(self):
        """
        Detect installed editors
        :param value:
        :return:
        """

        editors = list()

        if os.path.isfile('/usr/bin/kate'):
            editors.append(['Kate', '/usr/bin/kate %path% --line %line%'])

        if os.path.isfile('/usr/bin/gedit'):
            editors.append(['Gedit', '/usr/bin/gedit %path%'])

        if os.path.isfile('/usr/bin/leafpad'):
            editors.append(['Leafpad', '/usr/bin/leafpad %path% --jump=%line%'])

        phpStormSearch = subprocess.check_output("find $HOME -name 'phpstorm.sh' -type f", shell = True).strip()

        if os.path.isfile(phpStormSearch):
            editors.append(['phpStorm', phpStormSearch + ' %path% --line %line%'])

        return editors

    def setDefaultTextEditor(self, value):
        """
        Set text editor as default for use in phpBrowserIntegration
        :param value:
        :return:
        """

        value = value.strip()
        editors = self.detectEditors()

        for editor in editors:
            if editor[0].lower() == value.lower():
                self.app.config.setKey('ide.openFileCommand', editor[1])
                print('Done')
                sys.exit(0)

        print('Editor not found')
        sys.exit(1)

    def printDetectedEditors(self, value = ''):
        """
        List all detected editors
        :param value:
        :return:
        """

        editors = self.detectEditors()

        for editor in editors:
            print('+ ' + editor[0])

        sys.exit(0)


    def addArgs(self):
        """ Add application command-line arguments """

        self.createArgument('--text-editor', self.setDefaultTextEditor, '', 'Set text editor as default', required=False, action='store')
        self.createArgument('--detect-editors', self.printDetectedEditors, '', 'Detect text editors installed in system', required=False, action='store_false')