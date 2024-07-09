This project aims to create a simple overlay for a video game known as Elden Ring (but should work for all FromSoftware games). The program provides a death counter to the user to be able to keep track of how many times the user has died trying to take down enemies.

Requirements: Python3 (3.11.7), Windows 10/11, Various Python Libraries (included inside the requirements.txt file)

To set up the project follow these steps:

1. Download the whole project as a Zip. Once downloaded, create a folder to extract all the files into.
2. Open Command Prompt and navigate into the folder you extracted the files into.
3. Run the following command: "pip install -r requirements.txt". This will install all the required libraries. NOTE: You must have Python3 (Im using 3.11.7).
4. Run the overlay (at the moment only the SIFT based one works properly) via the command: "python overlay-sift.py"
5. Start playing and keeping track of your deaths. Good luck!!

For any issues create a thread and I will try my best to fix any bugs!

The project aims to take advantage of OpenCV's algorithms and win32's con/gui libraries. I am using the SIFT (Scale-Invariant Feature Transform) algorithm to match a pre-existing image with a specific phrase displayed on the screen. I am trying to make a version using the FLANN(Fast Library for Approximate Nearest Neighbors) algorithm as well but this has not been successful yet (once it is I will updated README). I use win32 to ensure that the window for the counter stays on top of all other applications.
