#
#
#   STONG note: this is an early stage, logic and variable names *might* change
#
#

# owner: Thomas Wagner (tom68) - please ask/discuss if you want non-trivial changes

# TODO: add more complete examples to help spec file engineers get the idea
# TODO: add copyright (CDDL?)


#
# EXAMPLE file for macro definitions for Solaris OS build version and distribution detection
#


#already included before?
%if %{?osdistro}
#we are already included
%else
%include osdistro.inc
%endif

# help the demo: pkgtool --interactive prep base-specs/osdistro.spec
Name: osdisto

%description
Demo the osdistro.inc use:

   pkgtool --interactive prep base-specs/osdistro.spec


Demo osdistro.inc in your own spec file:

Include this spec file by the "use" statement and do include include/osdistro.inc into your own spec file.
(remove the comment # signs)  
(the include osdistro.inc is always needed in your spec, the %use... and %osdistro.prep is only for demonstration)

Demo setup: Edit SFEyourspec.spec
#    #always do the include, this is the only line really required for normal operation
#    %include osdistro.inc

#    #optional for demoing inside your spec file's prep section or elsewhere
#    %use osdistro = osdistro.spec

then call the demo osdistop.prep inside your regular prep section to see at pkgbuild runtime what the result of the includefile osdistro.inc on your development machine is.

#    #optional for demoing inside your spec file is the call to "%osdistro.prep"
#    %prep    
#    %setup -q -n %name-%version    

#    %osdistro.prep

then run "pkgtool --interactive prep SFEyourspec.spec" and watch the variabled your might use in %if statements or other spec files code. enjoy.


%prep
echo "
osdistro: osbuild %{osbuild}
osdistro: SXCE %{SXCE}
osdistro: os2nnn %{os2nnn}
osdistro: os201005 %{os201005}
osdistro: os201003 %{os201003} deprecared, this release name was never used
osdistro: os200906 %{os200906}
osdistro: os200902 %{os200902}
osdistro: os200811 %{os200811}
osdistro: osdistrelnumber %{osdistrelnumber}
osdistro: osdistrelname   %{osdistrelname}
osdistro: osdet299999 %{osdet299999}
"



%changelog
* Jun  1 2010 - Thomas Wagner
- prettyprint the demoed variables (only one echo command), better %description
- check for already included osdistro.inc, else include it now for the demo
* May  5 2010 - Thomas Wagner
- add prep section to have a little debug output available. 
