git init
virtualenv --no-site-packages -p python --prompt="(kodi_addon)" venv
echo "/venv/" >> .gitignore && git add -f .gitignore
pip install git+https://github.com/romanvm/Kodistubs.git
zip -r kodi_addon.zip . -x "venv/*" -x ".git/*"


rtmp

rtmp://'+$('data-server')+'/rtmp',file:$('data-stream')
rtmpdump --rtmp "rtmp://data-server" --playpath "data-stream"


удалить файл из истории
git filter-branch --index-filter 'git rm --cached BIGFILE.ZIP --ignore-unmatch' --prune-empty --tag-name-filter cat -- --all

удалить каталог из истории
git filter-branch --force --index-filter 'git rm -r --cached --ignore-unmatch BIG/DIR' --prune-empty --tag-name-filter cat -- --all
