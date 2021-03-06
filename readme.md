# php-browser-integration

This is a small improvement written in Javascript and Python that allows clicking on filesystem paths in PHP and XDebug backtraces to open files in your favorite IDE.
Functionality could be extended by plugins to for example provide project-specific features like translated string language code.

## Requirements
- Panthera-Desktop Framework (https://github.com/Panthera-Framework/Panthera-Desktop)
- Tornado
- Python 2.7
- Linux / (propably) BSD

## Installation

1. Install Greasemonkey or Tampermonkey in your web browser of choice
2. Add script from client directory
3. Edit script to insert your domain where you are working on, by default its localhost
4. Go to server folder, run:
```bash
sudo python2.7 setup.py install
```

- Now check list of detected text editors using: 
```bash
php-browser-integration --detect-editors
```

- Set your editor, for phpStorm it would be for example:
```bash
php-browser-integration --text-editor phpStorm
```

- If your editor is not listed here, then set it manually, example:
```bash
# %line% parameter is optional, you don't have to enter this parameter
php-browser-integration --config-set ide.openFileCommand "/usr/bin/YourTextEditor %path% %line%"
```

- Run application
```bash
php-browser-integration

# or in background
php-browser-integration --daemonize
```

- Open ~/.php-browser-integration/config.json with text editor and set your project directories in "project.directories"
