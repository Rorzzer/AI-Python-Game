# Watch Your Back!

**COMP30024** *Artificial Intelligence*

Sarah Erfani, Matt Farrugia, Chris Leckie (*March 12, 2018*)

## Rules of the Game

*Watch Your Back!* is a fast-paced combat board game. You control a team of ruthless rogues engaged in a fight to the death against your enemies. Within the confines of a checkerboard there is no rulebook and no referee, and the easiest way to a cut down an enemy is to stab them in the back. Control your lawless warriors to jump and slash their way around the board surrounding and silencing your enemies until none remain. And, of course, *watch your back!*

[Full specifications](game-spec-2018.pdf)

## Project Part A: Massacre

In this part of the project, you will design and implement a Python program to analyse a board configuration for the game of *Watch Your Back!*. Before you read this specification, please make sure you have carefully read the "Rules of the Game" document.

The aims for Project Part A are for you and your project partner to refresh and extend your Python programming skills, explore some of the new algorithms we have met so far, and become more familiar with the mechanics of *Watch Your Back!*. This is also a chance for you to invest some time developing fundamental Python tools for working with the game: some of the functions and classes you create now may be helpful later when you are building your game playing agent for Project Part B.

### Task

You must write a Python 3.6 program that reads a text-based board configuration from input, and depending on a further input command, calculates one of the following:

 - The **number of available moves** for each player, or
 - a **sequence of moves** for White pieces that would eliminate all Black pieces assuming the Black pieces are unable to move.

The input format, the detail of these calculations, and the output format are explained in the [full specifications](partA-spec-2018.pdf).

### Assessment

Project Part A will be marked out of 8 points, and contribute 8% to your final mark for the
subject. Of the 8 points:

 - 2 points will be for the quality of your code: its structure (including good use of functions and classes) and readability (including good use of code comments).
 - 4 points will be for the correctness of your program, based on testing your program on a set of test cases. 2 of these points will be allocated to each of the two calculations your program must be able to perform.
 - 2 points will be for the accuracy and clarity of the discussion in your [**comments.txt**](comments.txt) file.

Note that even if you don't have a program that works correctly by the time of the deadline, you should submit anyway. You may be awarded some points for a reasonable attempt at the project.

You may make use of the library of classes provided by the AIMA textbook website if you wish, provided you make appropriate acknowledgements that you have made use of this library. Otherwise, for this part of the project, your program should not require any tools from outside the Python Standard Library.

Please note that questions and answers pertaining to the project will be available on the LMS  and will be considered as part of the specification for the project.

### Submission

One submission is required from each group. That is, one group member is responsible for submitting all of the necessary files that make up your group's solution.

You must submit a single compressed archive file (e.g. a `.zip` or `.tar.gz` file) containing all files making up your submission via the 'Project Part A Submission' item in the 'Assessments' section of the LMS.

This compressed file should contain **all Python files** required to run your program,  **and your comments.txt** file too. [Full specifications](partA-submit-2018.pdf).

#### Running your program

The entry point to your program should be a Python file called '[**parta.py**](parta.py)' (case sensitive). Note that you may structure your program over multiple Python files, but we will look for a file called parta.py when testing your program.

When marking your program, we will run your program with a command of the form:

```sh
python parta.py < input.txt
```

where

 - `python` is the name of a Python 3.6 interpreter, and
 - `input.txt` is the name of a file containing a board configuration and a command, as per the specification for Project Part A.

We will test your program on the Melbourne School of Engineering Student Unix machines (e.g. `dimefox.eng.unimelb.edu.au` or `nutmeg.eng.unimelb.edu.au`). If you develop your program with a different version of Python, it is your responsibility to make sure it runs correctly using Python 3.6 on the Student Unix machines.
