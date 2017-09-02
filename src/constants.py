from os.path import expanduser


TOP_PROFILE_FOLDER = expanduser('~') + '/.mozilla/firefox/'
PROFILE_REGEX = r'\w{8}\.'
USERCHROME_FOLDER = 'chrome'
USERCHROME_FILE = 'userChrome.css'

UCM_HEADER = '/* Start UCM section. Do not edit. */\n'
UCM_FOOTER = '/* End UCM section. */\n'
IMPORT_REGEX = '@import url\("(.*?\.css)"\);'
NAMESPACE_LINE = '@namespace url("http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul");\n'
