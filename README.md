# ConGen
[Kiwix](https://www.kiwix.org/en/about/) and [Wikipedia](https://en.wikipedia.org/) based *Context Generator*

### Usage
Download [wikipedia (zim files)](https://download.kiwix.org/zim/wikipedia/) and [kiwix-tools (v3.3.0)](https://download.kiwix.org/release/kiwix-tools/) and start web service.
```
./kiwix-server wikipedia/*.zim
```
Install all dependencies and start the program.
```
pip3 install -r requirements.txt
python3 congen.py "Harry Potter" --languages deu > output.txt
```