# Stop Pusheen my buttons #

I've always thought Pusheen was cute. Now I get to have random ASCII art of my favorite Pusheens show up on my terminal pop up whenever I open it!

I made this public because I thought people might enjoy it too :)

-------------------------------------------------------------------------------

## Results

![Heart Pusheen](https://github.com/IanQS/pusheen_the_limit/blob/master/imgSrc/2.png)

.....................,,,.,,,......................
.....................i@sr5s,......................
................,:,...:ir:,.......................
...............;sXs,.... .....::..................
.............,iXssXr,::.,,.,;rXA:.................
.............iXsssssrsXisr;s2Xsss,................
............:rss,,rXrrisssXr;iss;,................
..........,rrsssiisXi,.,:sXi,;Xsi::...............
.........,sXssssXXssXr;iXsssXXssssXi,.............
........,iXssssssssssXXXsssssssssssXs;,...........
........;XsssssssssssssssssssssssssssX;,..........
.......,Xsssssssssssssssssssssssssssss:,,.........
......,iXsssssssssssssssssssssssssssssrii:........
......:XsssssssssssssssssssssssssssssssXi:,.......
......;Xssssssssssssssssssssssssssssssssi::,......
.....,rXsssssssssssssssssssssssssssssssssss;......
.....,rsssssssssssssssssssssssssssssssssssss,.....
.....,rsssssssssssssssssssssssssssssssssssss,.....
.....,iXssssssssssssssssssssssssssssssssssss,.....
......;XssssssssssssssssssssssssssssssssssXi,.....
......,rXsssssssssssssssssssssssssssssssssX:......
.......,rXsssssssssssssssssssssssXXXXXsssXi.......
........,;rXXXXXXsXsssssXXsXsXXsrrrri;,;X;........
...........,:;i;:s:rsrrs;ir:sr,,,;:,:i,,,.........
.............. ..,.......,,....,,::,,,............
..................................................
..................................................
............rr......3ii...........................



---

## Installation
If you use virtual environments (and IMO you should) just run

`mkvirtualenv pusheen -r packages.txt`

assuming you have [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html) installed. Find out more about [virtualenv](https://virtualenv.pypa.io/en/stable/)


-------------------------------------------------------------------------------
## Usage

#### Python Script

```
rm -rf imgDest; rm -rf ~/imgDest; rm -rf ~/.pusheens; python __main__.py; cp -r imgDest ~/imgDest; mv ~/imgDest ~/.pusheens
```

Removes any lingering images you've got stored, then runs the script with the default arguments and copies the results to your desktop folder from which you can source from your bashrc.

#### Short blurbs of Python

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

---

#### Shell Commands

add to the bottom of your .rc file so that it runs on every shell startup

a) zsh

```
rand() REPLY=$RANDOM
cat ~/.pusheens/*(o+rand[1])
```


b) bash or whatever. Who knows who cares move to zsh


```
find ~/.pusheens -type f -print0 | shuf -zn1 | xargs -0 cat
```

In all seriousness, please know that this bash script [isn't safe](https://askubuntu.com/questions/849665/cat-a-random-file-in-terminal)

---

## Future Work

You're joking, right...?

0) Add in [Gabe the dog](https://www.youtube.com/watch?v=c--etqIJcow) (RIP in pupper heaven) and the famous doge dog

1) Mask R-CNN to segment the image and if it matches a dog or cat we'll take just that and mask everything else out which is bloody overkill especially for Pusheen
