#
# Macro definitions for Solaris packages
#
# Copyright 2009 Sun Microsystems, Inc.
#

# note this fails havily if you are "BFU"ing your box
# (if you don't use BFU / don't know what BFU is, you don't need to take care of)


# detect os distro and os build version if possible
# distinguish between SXCE and OS20nn.nn, set distro numbers for "osbuild > nnn" logic
# try to detect the distro release in case of OS20nn.nn
# and provide flags e.g. %OS200902

# see also the include file "packagenamemakros.inc" for
# already predefined "BuildRequires" and "Requires" depending
# on the distro and build number, leveraging the detection from 
# this osversion.inc include file
# should simplify sharing spec files between SXCE and OS20nn.nn


# usage/examples:
# if you depend on a package wich for instance got some day a rename:
# (or dissapeared, newly introduced, merged into another package
# this is not limited to these examples (think of switching off SVR4 package
# scripting, ...).
#
# %if %(expr %{osbuild} '>=' 100)
# BuildRequires: SUNWnewname
# %else
# BuildRequires: SUNWoldname
# %endif

# *if* we are on OS20nn.nn *and* build is younger|equal then 118
# %if %OS2nnn %( expr %osbuild '>=' 118 )
# BuildRequires: newpackagename
# %else
# BuildRequires: SUNWoldname
# %endif

# same as above but based on the OS20nn.nn distro, example OS2009.06 and above
# %if %( expr %OS2nnndistro '>=' 200906 && echo 1 || echo 0 )
# BuildRequires: newpackagename
# %else
# BuildRequires: SUNWoldname
# %endif

### end of examples
### rules below need extensions with every major distro release

%define osbuild %(uname -v | sed -e 's/[A-z_]//g')

# see if we are on old SVR4 release
%define SXCE %( egrep "Solaris Express Community Edition" /etc/release  && echo 1 || echo 0 )


#switches for major distro releases
# OS2nnn is defined 1 if we can detect the OpenSolaris (IPS based) distro
# 
# an estimate is done to tell which distro release is present
# OS2008.11 OS2009.06 OS2009.11 OS2010.02
# OS200811  OS200906  OS200911  OS201002

#numbers for each major distro release are stroed in %OS2nnnversion

#Flags - who knows what that's worth for
#set defaults to null - reverse order to catch youngest distro first 
#and then used to skip the other detection rules for older releases
%define OS201002 0
%define OS200906 0
%define OS200902 0
%define OS200811 0


# one of the IPS style OpenSolaris distro releases is present if OS2nnn set to "1"
# set default to "0" with is good
%define OS2nnn        0

# make your logic major distro release dependent by  %if %( expr %OS2nnndistro '>=' 200906 )
# set default to "0" with is good
%define OS2nnndistro 0

# Note OS299999detection is a helper variable. Specs should use %if %OS2nnn ... and %OS2nnndistro
# Make default to "1" to enable the OS20nn.nn detection steps below.
# for readability see separated %if where a present %SXCE resets this switch to "0" and disables all remaining checks
%define OS299999detection 1

# we are on SXCE, so skip the all other OS2nnn detection rules and leave %OS**** defaults at "0"
%if %SCXE
#no more work to do
%define OS299999detection 0
%endif


# try detecting the distro release we are on
# might need more fine grained rules some day?

#(preview OS2010.02)
#e.g. OpenSolaris Development snv_118 X86
#we decide on the "ON" kernel build release

%if %OS299999detection %(expr %{osbuild} '>=' 118) %( egrep "OpenSolaris Develop" /etc/release > /dev/null  && echo 1 || echo 0) 
%define OS2nnn 1
%define OS2nnndistro 201002
#this was the last check, skip all others
%define OS299999detection 0
%endif


#(OS2009.06)
#e.g. OpenSolaris 2009.06 snv_111b X86

%if %OS299999detection %(expr %{osbuild} '>=' 111) %( egrep "OpenSolaris 2[0-9][0-9][0-9]" /etc/release > /dev/null  && echo 1 || echo 0) 
%define OS2nnn 1
%define OS2nnndistro 200906
#this was the last check, skip all others
%define OS299999detection 0
%endif


##BELOW need to check build numbers alingment to osbuild numbers for remaining distro releases

####(OS2009.02)
####e.g. OpenSolaris Development snv_97 X86
###
###%if %OS299999detection  %(expr %{osbuild} '>=' 97) %( egrep ÖpenSolaris 2[0-9][0-9][0-9]" /etc/release > /dev/null  && echo 1 || echo 0)
###%define OS2nnn 1
###%define OS2nnnversion 200806
####this was the last check, skip all others
###%define OS299999detection 0
###%endif


### bail out, detection of the OS2nnn distribution failed!
%if %OS299999detection
echo "Error. Detection of OS Distribution failed in osdistro.inc"
exit 1
%endif

%changelog
* Aug 27 2009 - Thomas Wagner
- initial - drafting the idea, bugs are the only feature of this include file
