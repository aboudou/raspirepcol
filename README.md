RasPiRepCol
===========

RasPiRepCol (“RepCol” meanings Repeat Colors) is a project for the [Raspberry Pi](http://www.raspberrypi.org) implementing a clone of the electronic game [Simon](http://en.wikipedia.org/wiki/Simon_(game)).

You can have more information into “doc” folder.

* [Project's website](https://goddess-gate.com/dc2/index.php/pages/raspirepcol.en)
* [Youtube video](http://www.youtube.com/watch?v=H_xmR35Ws0w)

Requirements
------------

* First of all : a Raspberry Pi
* LED and resistors to build the assembly. Assembly instructions are available at the following URL: [https://goddess-gate.com/dc2/index.php/pages/raspirepcol.en](https://goddess-gate.com/dc2/index.php/pages/raspirepcol.en)
* Python (with Debian / Raspbian : packages "python" and "python-dev")
* RPi.GPIO library (0.3.1a or newer) from [http://pypi.python.org/pypi/RPi.GPIO](http://pypi.python.org/pypi/RPi.GPIO)

To help you with the assembly, you may refer to the following files :

* raspirepcol.sch : the circuit diagram to open with EAGLE 
  ([http://www.cadsoft.de/freeware.htm](http://www.cadsoft.de/freeware.htm))
* raspirepcol.fzz : the assembly mockup to open with Fritzing 
  ([http://fritzing.org/](http://fritzing.org/))


How to use RasPiRepCol
----------------------

You'll first have to build the assembly, and plug it to the Raspberry Pi
  (check [https://goddess-gate.com/dc2/index.php/pages/raspirepcol.en](https://goddess-gate.com/dc2/index.php/pages/raspirepcol.en) for more information).

When you're done, just launch RasPiRepCol with `python ./raspirepcol.py` as
  root user and start playing :-) When you want / need to stop playing, just
  hit `Ctrl + C` to quit.


How to play
-----------
When the game is started, all LED blink three time. Then you have to choose 
game difficulty (aka game speed) : press one of the four switches, and if you
think your choice is the good one, press the same button. Otherwise, press
another switch.

Then one random LED blink once, and the game waits for the player to push the 
switch in front of it.

If the player push the correct switch, the game blinks again the first LED, then
blinks another random one, and wait for the player to replay the sequence. And
so on...

If the player press the wrong button, all LED blink three time, and the game
restarts from the beginning.

When you want to skip the game, just hit `Ctrl + C` to quit.

