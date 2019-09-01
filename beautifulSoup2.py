import os, pathlib, re, shutil
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# print(os.environ.get("HOME"))
_trgtDir = "{}\{}\{}".format(pathlib.Path.home(), "Desktop", "img")

# print(_trgtDir) -> 출력하면 C:\Users\Administrator\Desktop\img
# but 실제값은 C:\\Users\\Administrator\\Desktop\\img 이다. 자동으로 역슬래쉬 하나식 더 붙더라
# 역슬레쉬 두개로 들어가야 한다. 하나로 들어가면 \User 에서 유니코드로 인식해서 오류난다.

# makeing for directory of scraping images
if os.path.exists(_trgtDir) :
    # os.rmdir(_trgtDir) if not empty, raising error
    shutil.rmtree(_trgtDir) # Delete directory and file

os.mkdir(_trgtDir)

print("Scraping Dir :", _trgtDir)
print()

_url = input("Enter url : ")
print()

_counts = 0;
try :
    _request = urllib.request.Request(_url, headers={'User-Agent':'Mozilla/5.0'})
    _response = urllib.request.urlopen(_request, context=ctx)
    _soup = BeautifulSoup(_response, 'html.parser') # 첫번째 인자는 unicode, utf-8 byte 뭐든 된다.
    _imgs = _soup.find_all("img")

    # enumerate makes and returns the tuple that has sequence.
    for i, _img in enumerate(_imgs) :
        _srcUrl = _img.get("src")

        # https://s.pstatic.net/static/www/mobile/edit/2019/0829/mobile_180126994547.jpg?345345
        # //s.pstatic.net/static/www/mobile/edit/2019/0829/mobile_180126994547.jpg?345345
        # /static/www/mobile/edit/2019/0829/mobile_180126994547.jpg?345345
        # /mobile_180126994547.jpg?345345
        # ./mobile_180126994547.jpg?345345
        # mobile_180126994547.jpg?345345
        # finadall returns tuple [('', '', '', '')]
        _groups         = re.findall(r"^(http[s]?)?(?::)?(?://)?(\w+\.?\w+\.\w+)?(.*/)?(\w+\.[^?]+).*$", _srcUrl)[0]
        _schema         = _request.type if not _groups[0] else _groups[0]
        _domain         = _request.host if not _groups[1] else _groups[1]
        _middlePath     = _groups[2]
        _fileName       = _groups[3]

        # validate filename one more time
        _match = re.match(r"^\w+\.\w+$", _fileName)
        if _match is None :
            continue

        _srcAbsUrl      = "{}://{}{}{}".format(_schema, _domain, _middlePath, _fileName)

        print(i, _fileName, _srcUrl, _srcAbsUrl)
        urllib.request.urlretrieve(_srcAbsUrl, "{}\{}".format(_trgtDir, _fileName))    # 역슬레쉬 하나로 해도 되고 두개로 해도 된다.
        _counts += 1

except Exception as e :
    print("Exception :", e)
    #quit()

print()
print("{} saved file".format(_counts))
