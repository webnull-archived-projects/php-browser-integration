import tornado.ioloop
import tornado.web
import json
import base64
import os
import sys
import subprocess
import binascii
import phpBrowserIntegration
import socket

class phpBrowserIntegrationHandler(tornado.web.RequestHandler):
    ideOpenFileCommand = '/usr/local/bin/phpstorm %path% --line %line%'
    remoteHosts = ['localhost', '::1', '127.0.0.1']
    kernel = None

    def writeHeaders(self):
        """
        Send list of allowed hosts to browser
        :return:
        """

        self.set_header('Access-Control-Allow-Origin', ",".join(self.remoteHosts))

    def respond(self, responseArray):
        """
        Write a response to client
        :param responseArray:
        :return:
        """

        if 'status' in responseArray and 'code' in responseArray and (responseArray['status'] == 'false' or responseArray['status'] == 'failed'):

            withMessage = ''

            if 'message' in responseArray:
                withMessage = ', with message "' + responseArray['message'] + '"'

            self.kernel.logging.output('[' + self.request.remote_ip + '] Invalid request, sent "' + responseArray['code'] + '" code to the browser' + withMessage, 'webserver')

        self.write(json.dumps(responseArray, sort_keys=True, indent=4, separators=(',', ': ')))

    def validateClient(self):
        """
        Security related features
        :return:
        """

        ## Validate client's IP address
        if not self.request.remote_ip in self.remoteHosts:
            self.kernel.logging.output('Client ' + self.request.remote_ip + ' was rejected due to unknown remote host', 'webserver')

            self.respond({
                'status': 'false',
                'code': 'not-authorized'
            })
            return

        token = None

        ## Client token passed via X-Auth-Token header or a GET parameter - "token"
        if self.request.headers.get('X-Auth-Token'):
            token = self.request.headers.get('X-Auth-Token')
        elif self.get_argument('token'):
            token = self.get_argument('token')

        ## Check if user has passed a valid authorization token/key
        if self.kernel.config.getKey('security.tokens') and not str(token) in self.kernel.config.getKey('security.tokens'):
            self.kernel.logging.output('Token "' + str(token) + '" not recognized', 'webserver')

            self.respond({
                'status': 'false',
                'code': 'not-authorized',
                'message': 'Token code not recognized'
            })
            return

        return True


    def get(self, path = ''):
        """
        Supports get method
        :param path: Absolute path to file in a filesystem
        :return:
        """

        self.kernel = phpBrowserIntegration.application.getInstance()

        ## Default configuration
        self.ideOpenFileCommand = self.kernel.config.getKey('ide.openFileCommand', '/usr/bin/kate %path% --line %line%')
        self.remoteHosts = self.kernel.config.getKey('allowedHosts', ['localhost', '::1', '127.0.0.1'])
        self.kernel.hooking.execute('app.request.configure', self)

        ## Write required headers to browser
        self.writeHeaders()

        self.kernel.logging.output('Client ' + self.request.remote_ip + ' connected and requested /' + str(path) + ' path', 'webserver')

        ## Validate user if its connecting from allowed remote/local host
        if not self.validateClient():
            return

        if not path:
            self.respond({
                'status': 'false',
                'code': 'api-command-not-found'
            })

            return

        exp = path.split('/')

        if exp[0] == 'open-project-file' and len(exp) >= 3:
            try:
                return self.openProjectFile(base64.decodestring(exp[1]), exp[2])
            except binascii.Error:
                self.respond({
                    'status': 'false',
                    'message': 'Invalid base64 encoded data',
                    'code': 'invalid-data'
                })

                return None

        self.respond({
            'status': 'false',
            'code': 'api-command-not-found'
        })

        return



    def openProjectFile(self, path, line):
        """
        Open a IDE editor on selected file and line
        :param path: Input file path
        :param line: Line number
        :return: None
        """

        path, line = self.kernel.hooking.execute('app.request.openProjectFile', [path, line])

        try:
            int(line)
        except ValueError:
            print('Invalid line passed')
            line = 0

        ## Restrict access only to project directories
        baseDirs = self.kernel.config.getKey('project.directories', [
            '/var/www/',
            '/srv/http/'
        ])

        rPath = os.path.realpath(path)
        found = False

        ## Check if file exists
        if not os.path.isfile(rPath):
            self.respond({
                'status': 'false',
                'message': 'File not found',
                'code': 'file-not-found'
            })
            return

        for baseDir in baseDirs:
            if rPath.find(os.path.realpath(baseDir)) == 0:
                found = True

        ## If file not found in base project directories
        if not found:
            self.respond({
                'status': 'false',
                'message': 'File not found',
                'code': 'file-not-found'
            })
            return

        command = self.ideOpenFileCommand.replace('%path%', rPath).replace('%line%', str(int(line))) + ' & > /dev/null &2>/dev/null'
        self.kernel.logging.output("executing: " + command, 'webserver')

        subprocess.Popen([command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

        self.respond({
            'status': 'success'
        })
        return

def run():
    app = phpBrowserIntegration.application.getInstance()

    application = tornado.web.Application([
        (r"/(.*)", phpBrowserIntegrationHandler),
    ], default_host = app.config.getKey('listen.host', ''))

    try:
        application.listen(app.config.getKey('listen.port', 8161))
        tornado.ioloop.IOLoop.instance().start()
        app.logging.output('The server is running', 'webserver')
    except socket.error as e:
        print('Cannot run server, ' + str(e))
        sys.exit(1)

    return application



if __name__ == "__main__":
    run()
