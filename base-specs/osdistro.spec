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

%description
Include this spec file togheter with the include/osdistro.inc into your owen spec file:

    %include osdistro.inc
    %use osdistro = osdistro.spec

then call the prep function to see at pkgbuild runtime what the result on your development machine is.

    %prep
    %setup -q -n %name-%version

    %osdistro.prep

then run the pkgbuild/pkgtool with at least the "pkltool prep your.spec" or "pkgbuild -bp your.spec" step and enjoy.

%prep
echo "osdistro: osbuild %{osbuild}"
echo "osdistro: SXCE %{SXCE}"
echo "osdistro: os201003 %{os201003}"
echo "osdistro: os200906 %{os200906}"
echo "osdistro: os200902 %{os200902}"
echo "osdistro: os200811 %{os200811}"
echo "osdistro: osdistrelnumber %{osdistrelnumber}"
echo "osdistro: osdistrelname   %{osdistrelname}"
echo "osdistro: osdet299999 %{osdet299999}"
#echo "osdistro: xx %{}"
#echo "osdistro: xx %{}"
#echo "osdistro: xx %{}"



%changelog
* May  5 2010 - Thomas Wagner
- add prep section to have a little debug output available. 
