############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/shahzebsiddiqui/buildtest 
# 
#  This file is part of buildtest. 
# 
#    buildtest is free software: you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by 
#    the Free Software Foundation, either version 3 of the License, or 
#    (at your option) any later version. 
# 
#    buildtest is distributed in the hope that it will be useful, 
#    but WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#    GNU General Public License for more details. 
# 
#    You should have received a copy of the GNU General Public License 
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>. 
############################################################################# 
from setup import *
def add_arg_to_runcmd(runcmd,arglist):
        # add each argument to runcmd
        for arg in arglist:
        # skip argument if value is not specified, by default set to None
                if arg == None:
                        continue
                # in case argument is not a string, convert it anyways
                runcmd+= " " + str(arg)
        return runcmd


def load_modules(software,toolchain):
        """
        return a string that loads the software and toolchain module. 
        """
        # for dummy toolchain you can load software directly. Ensure a clean environment by running module purge
        if toolchain[0] == "dummy":
                header="""
#!/bin/sh
module purge
module load """ + software[0] + "/" + software[1] + """
"""
        else:
                header="""
#!/bin/sh
module purge
module load """ + toolchain[0] + "/" + toolchain[1] + """
module load """ + software[0] + "/" + software[1] + """
"""

        return header


def print_dictionary(dictionary):
        """
        prints the content of dictionary
        """
        for key in dictionary:
                print key, sset(dictionary[key])

def print_set(setcollection):
        """
        prints the content of set 
        """
        for item in setcollection:
                print item
		BUILDTEST_LOGCONTENT.append(item + "\n")
class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

