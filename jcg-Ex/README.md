# About this Branch
This branch contains example code of how to do certain things.
Different commits in this branch contain different examples.
The full list of examples can be found below.  To use any particuar example, simply checkout that commit and run the preactivate.sh script:

>    `$ sudo sh preactivate.sh`



# This Example
This example details how Flask and Jinja2 work together to render dynamic HTML pages.  To use this, launch the server from the root directory:

>    `$ ./server.py`

 ...and visit any webpage at localhost:5000/

This will render a html webpage using a Jinja2 template.  The template is being populated with variables from the Flask app.


# List of Previous Examples
To see the full list of examples, git pul the latest commit and view that Readme.  The list of examples (in reverse chronological order, not including this one, as of this commit) are:

8156bc3 : using flask with pymongo and mongokit