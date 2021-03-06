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
from parser.args import *
from tools.generic import *
from tools.file import *
import shutil 

def init_CMakeList(filename):
        """
        This is the content of BUILDTEST_ROOT/CMakeLists.txt
        """
        header = """ 
cmake_minimum_required(VERSION 2.8)
include(CTest)
ENABLE_TESTING()
add_subdirectory(""" + BUILDTEST_TESTDIR + ")"
        fd=open(filename,'w')
        fd.write(header)
        fd.close()


def update_CMakeLists(filename,tag, verbose):
        """
        used for writing CMakeLists.txt with tag <software>, <version>, & toolchain
        """
        fd=open(filename,'r')
        content=fd.read().strip().split("\n")
        cmd="add_subdirectory("+tag+")"
        if cmd not in content:
                fd.close()
                fd=open(filename,'a')
                fd.write(cmd+"\n")
                fd.close()
                if verbose >= 1:
                        print "writing:", cmd, "to file:",filename
        else:
                fd.close()

def add_test_to_CMakeLists(appname,appver,tcname,tcver,app_destdir,subdir,cmakelist,testname):
	""" update CMakeLists.txt with add_test command to allow ctest to run test """

	fd=open(cmakelist,'a')
	add_test_str=""

        # if YAML files are in subdirectory of config directory then update CMakeList
        # in app_destdir to add tag "add_subdirectory" for subdirectory so CMakeList
        # can find tests in subdirectory
	if subdir != "":
		# only update the app_destdir/CMakeLists.txt if subdirectory doesn't exist. This avoids
		# writing duplicate values when there are multiple tests in subdirectory
		parent_cmakelist = os.path.join(app_destdir,"CMakeLists.txt")
               	cmake_content="add_subdirectory("+subdir+") \n"
	 	ret = string_in_file(cmake_content,parent_cmakelist)
		if ret == False:
	               	fd1=open(parent_cmakelist,'a')
		        fd1.write(cmake_content)
        	       	fd1.close()

                # the string add_test in CMakeLists allows you to test script with ctest. The NAME tag is 
                # <name>-<version>-<toolchain-name>-<toolchain-version>-<subdir>-<testname>. This
                # naming scheme should allow buildtest to reuse same YAML configs for multiple version
                # built with any toolchains. Subdirectories come in handy when you need to organize tests 
		# effectively to avoid naming conflict
      		
		add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"      + subdir + "-" + testname + "\t COMMAND sh " +  testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	else:
         	add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"  + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	fd.write(add_test_str)
        fd.close()
	BUILDTEST_LOGCONTENT.append("Updating File " + cmakelist + " with: " + add_test_str + "\n")

def setup_software_cmake(software,toolchain,args_dict):
	verbose=get_arg_verbose(args_dict)
	name,version=software
	toolchain_name,toolchain_version=toolchain

	 # if top level software directory is not present, create it
        test_ebapp_dir=os.path.join(BUILDTEST_TESTDIR,"ebapp")

        # variables to reference each subdirectory in <software>/<version>/<toolchain-name>/<toolchain-version>
        test_name_dir=os.path.join(test_ebapp_dir,name)
        test_version_dir=os.path.join(test_name_dir,version)
        test_toolchain_name_dir=os.path.join(test_version_dir,toolchain_name)
        test_toolchain_version_dir=os.path.join(test_toolchain_name_dir,toolchain_version)

        # BUILDTEST_TESTDIR/CMakeLists.txt
        test_cmakelist = os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")

        # BUILDTEST_TESTDIR/ebapps/CMakeLists.txt
        test_ebapp_cmakelist = os.path.join(test_ebapp_dir,"CMakeLists.txt")

        # CMakeLists.txt files in <software>/<version>/<toolchain-name>/<toolchain-version>
        test_name_cmakelist = os.path.join(test_name_dir,"CMakeLists.txt")
        test_version_cmakelist = os.path.join(test_version_dir,"CMakeLists.txt")
        test_toolchain_name_cmakelist = os.path.join(test_toolchain_name_dir,"CMakeLists.txt")
        test_toolchain_version_cmakelist = os.path.join(test_toolchain_version_dir,"CMakeLists.txt")

	test_destdir=test_toolchain_version_dir

	BUILDTEST_LOGCONTENT.append(" Variables Assignments \n")
        BUILDTEST_LOGCONTENT.append("test_ebapp_dir = " + test_ebapp_dir + "\n")
        BUILDTEST_LOGCONTENT.append("test_name_dir = " + test_name_dir + "\n")
        BUILDTEST_LOGCONTENT.append("test_version_dir = " + test_version_dir + "\n")
        BUILDTEST_LOGCONTENT.append("test_toolchain_name_dir = " + test_toolchain_name_dir + "\n")
        BUILDTEST_LOGCONTENT.append("test_toolchain_version_dir = " + test_toolchain_version_dir + "\n")
        BUILDTEST_LOGCONTENT.append("test_cmakelist = " + test_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("test_name_cmakelist = " +test_name_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("test_version_cmakelist = " +test_version_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("test_toolchain_name_cmakelist = " +test_toolchain_name_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("test_toolchain_version_cmakelist = " +test_toolchain_version_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("test_destdir = " + test_destdir + "\n")

        # if test directory exist, delete and recreate it inorder for reproducible test builds
        if os.path.isdir(test_destdir):
                shutil.rmtree(test_destdir)
                BUILDTEST_LOGCONTENT.append("removing directory " + test_destdir + "\n")

	 # create directories if they don't exist
        # Directory Format: <software>/<version>/toolchain-name>/<toolchain-version>
        create_dir(test_ebapp_dir,verbose)
        create_dir(test_name_dir,verbose)
        create_dir(test_version_dir,verbose)
        create_dir(test_toolchain_name_dir,verbose)
        create_dir(test_toolchain_version_dir,verbose)

        # create CMakeList.txt file in each directory of <software>/<version>/<toolchain-name>/<toolchain-version> if it doesn't exist
        create_file(test_ebapp_cmakelist,verbose)

        create_file(test_name_cmakelist,verbose)
        create_file(test_version_cmakelist,verbose)
        create_file(test_toolchain_name_cmakelist,verbose)
        create_file(test_toolchain_version_cmakelist,verbose)

	 # update CMakeLists.txt with tags add_subdirectory(ebapp)
        update_CMakeLists(test_cmakelist,"ebapp",verbose)

        # update CMakeLists.txt with tags add_subdirectory(X) where X=name|version|toolchain-name|toolchain-version
        update_CMakeLists(test_ebapp_cmakelist,name,verbose)
        update_CMakeLists(test_name_cmakelist,version,verbose)
        update_CMakeLists(test_version_cmakelist,toolchain_name,verbose)
        update_CMakeLists(test_toolchain_name_cmakelist,toolchain_version,verbose)


        BUILDTEST_LOGCONTENT.append("Creating directory: " + test_ebapp_dir + "\n")
        BUILDTEST_LOGCONTENT.append("Creating directory: " + test_name_dir + "\n")
        BUILDTEST_LOGCONTENT.append("Creating directory: " + test_version_dir + "\n")
        BUILDTEST_LOGCONTENT.append("Creating directory: " + test_toolchain_name_dir + "\n")
        BUILDTEST_LOGCONTENT.append("Creating directory: " + test_toolchain_version_dir + "\n")

        BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt file: " + test_ebapp_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt file: " + test_name_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt file: " + test_version_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt file: " + test_toolchain_name_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt file: " + test_toolchain_version_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("Updating " + test_cmakelist + " with add_subdirectory(ebapp) \n")
        BUILDTEST_LOGCONTENT.append( "Updating " + test_ebapp_cmakelist + " with add_subdirectory("+name+")\n")
        BUILDTEST_LOGCONTENT.append("Updating " + test_name_cmakelist + " with add_subdirectory("+version+")\n")
        BUILDTEST_LOGCONTENT.append( "Updating " + test_version_cmakelist + " with add_subdirectory("+toolchain_name+")\n")
        BUILDTEST_LOGCONTENT.append("Updating " + test_toolchain_name_cmakelist + " with add_subdirectory("+toolchain_version+")\n")

	return test_destdir,test_toolchain_version_cmakelist

def setup_system_cmake(args_dict,pkg):
	 # top level system directory and system package directory
        test_system_dir=os.path.join(BUILDTEST_TESTDIR,"system")
        test_destdir=os.path.join(BUILDTEST_TESTDIR,"system",pkg)

        # top level CMakeLists.txt in testing directory
        test_cmakelist = os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")

        # CMakeLists.txt that contains all system package directories to process
        test_cmakelist_pkg = os.path.join(BUILDTEST_TESTDIR,"system","CMakeLists.txt")

        # CMakeLists.txt that contais the actual tests (add_test)
        test_cmakelist_destdir=os.path.join(test_destdir,"CMakeLists.txt")

	BUILDTEST_LOGCONTENT.append("------------------------------------------------\n")
	BUILDTEST_LOGCONTENT.append("function: setup_system_cmake \n ")
	BUILDTEST_LOGCONTENT.append("------------------------------------------------\n")
        BUILDTEST_LOGCONTENT.append(" Variables Assignments \n")
        BUILDTEST_LOGCONTENT.append("test_system_dir = " + test_system_dir + "\n")
        BUILDTEST_LOGCONTENT.append("test_destdir = " + test_destdir + "\n")
        BUILDTEST_LOGCONTENT.append("test_cmakelist = " + test_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("test_cmakelist_pkg = " + test_cmakelist_pkg + "\n")
        BUILDTEST_LOGCONTENT.append("test_cmakelist_destdir = " + test_cmakelist_destdir + "\n")

        # if testdirectory exist, delete and recreate it inorder for reproducible test builds
        if os.path.isdir(test_destdir):
                shutil.rmtree(test_destdir)
                BUILDTEST_LOGCONTENT.append("removing directory " + test_destdir + "\n")

	verbose=get_arg_verbose(args_dict)
        # create the directories if they don't exist
        create_dir(test_system_dir,verbose)
        create_dir(test_destdir,verbose)

        # create CMakeLists.txt files if they are not present
        create_file(test_cmakelist,verbose)
        create_file(test_cmakelist_pkg,verbose)
        create_file(test_cmakelist_destdir,verbose)

        # update the CMakeLists.txt with the tag add_subdirectory(system) 
        update_CMakeLists(test_cmakelist,"system",verbose)


        BUILDTEST_LOGCONTENT.append("Creating directory: " + test_system_dir + "\n")
        BUILDTEST_LOGCONTENT.append("Creating directory: " + test_destdir + "\n")
	BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt File: " + test_cmakelist + "\n")
        BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt File: " + test_cmakelist_pkg + "\n")
        BUILDTEST_LOGCONTENT.append("Creating CMakeLists.txt File: " + test_cmakelist_destdir + "\n")

        BUILDTEST_LOGCONTENT.append("Updating " + test_cmakelist + " with add_subdirectory(system) \n")
        BUILDTEST_LOGCONTENT.append("Updating " + test_cmakelist_pkg + " with add_subdirectory("+pkg+") \n")
        # update CMakeLists.txt with the tag add_subdirectory(pkg) where pkg is the application name
        update_CMakeLists(test_cmakelist_pkg,pkg,verbose)

	return test_destdir,test_cmakelist_destdir
