## Stop Pusheen my buttons ##

I've always thought Pusheen was cute. Now I get to have images of Pusheen on my terminal pop up whenever I open it!

-------------------------------------------------------------------------------

# Installation
If you use virtual environments (and IMO you should) just run

`mkvirtualenv pusheen -r packages.txt`

assuming you have [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html) installed. Find out more about [virtualenv](https://virtualenv.pypa.io/en/stable/)


-------------------------------------------------------------------------------
# Usage

1) Python Script

```
rm -rf imgDest; rm -rf ~/imgDest; rm -rf ~/.pusheens; python __main__.py; cp -r imgDest ~/imgDest; mv ~/imgDest ~/.pusheens
```

Removes any lingering images you've got stored, then runs the script with the default arguments and copies the results to your desktop folder from which you can source from your bashrc.

```python
# Tuple to resize the pusheen images to
# Defaults to 80,40
python __main__.py -sh 80, 40

# Gets the images from folder or single file called fromhere
# Defaults to imgSrc
python __main__.py -sf fromHere

# Debug mode - stores the resized version, and prints the ASCII art to your terminal
# Defaults to False
python __main__.py -db True

# remove background - a misnomer as it really just makes the background 'sane' so that it outputs nicely on terminal
# Defaults to True
python __main__.py -rm True

```

2) Shell command

```
rand() REPLY=$RANDOM
cat ~/.pusheens/*(o+rand[1])
```
