# cuatro
Cuatro is a 3D version of connect 4 game coded in Python and pygame.
type: "python cuatro.py" in the command line to launch the script. The intro of the game offers guidance on how to palay.
Cuatro can handle different game sizes (how many bricks hold the game per dimension) and how many bricks in a line that consitutues a win. The defaults are a size of 5 and a win of four but they can be modified passing the appropriate arguments. For example typye: "python cuatro.py --game_size 6 --game_win 5"
The visualization of the game can be changed by passing specific arguments such as the camera position, how far is the board from the camera or where is the light. Also the size of the window game can be changed through arguments (the default is to adjust to the screen resolution). The available arguments can be accessed by typing: "python cuatro.py -h" althoug I have not commented them yet to build a real help.
You will need at least one game-pad plugged to play (I have not coded keybord control). If no game-pad is plugged you will just watch Cuatro play against itself.
The project has been coded in python 2.7 but it should work in python 3 as well, and both in linux and windows.
Dependencies are pygame and numpy.
Watch this videos in youtube for a demo: 
https://youtu.be/uukpv5mSabM
https://youtu.be/6B9cSALACOA
