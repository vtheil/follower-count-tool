# Follower Count Tool
This tool retrieves Follower and Following information for (currently) Instagram profiles without having to navigate through their app/ website.

## Usage
```
usage: follower-count.py [-h] --username USERNAME

Follower Count Tool is a tool that looks up Instagram profile information for a requested user.

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME, -u USERNAME
                        The Instagram username to look up
```

## Example
Below is an example for looking up the user [kevin](https://www.instagram.com/kevin/)
```
% ./follower-count.py -u kevin 
kevin
Following - 532
Followers - 7901877
```