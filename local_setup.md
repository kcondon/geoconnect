# Local Installation Instructions

GeoConnect works as a middle layer, allowing [Dataverse](http://datascience.iq.harvard.edu/dataverse) files to be visualized on the [Harvard WorldMap](http://worldmap.harvard.edu/).

*caveat*: Directions not too windows friendly...

## Prerequisites

### Install [pip](http://pip.readthedocs.org/en/latest/installing.html)

* use sudo if needed  (mac users, use sudo)
* if on Windows, make sure [python](https://www.python.org/downloads/) is installed.

### Install [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation)

* The virtualenvwrapper may be installed via pip:

    ```
    pip install virtualenvwrapper
    ```

  * On windows, either install [virtualenvwrapper-win-1.1.5](https://pypi.python.org/pypi/virtualenvwrapper-win) or [cygwin](https://www.cygwin.com/).

* Set the shell to use virtualenvwrapper. (shell startup file)[http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file]
  - For Mac users:
    1. Open a new terminal
    2. Open your ```.bash_profile``` for editing
    3. Add these lines
      
        ```
        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/Devel
        source /usr/local/bin/virtualenvwrapper.sh
        ```

  - If you're using windows, [this](http://stackoverflow.com/questions/2615968/installing-virtualenvwrapper-on-windows) might be helpful.

### Make sure git is installed locally with access to github

- Recommended: [Install Github Desktop](https://desktop.github.com/)