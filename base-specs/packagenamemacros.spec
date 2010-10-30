#
#
#   STRONG note: this is an early stage, logic and variable names *might* change
#
#

# owner: Thomas Wagner (tom68) - please ask/discuss if you want non-trivial changes

# TODO: add more complete examples to help spec file engineers get the idea
# TODO: add copyright (CDDL?)


#
# EXAMPLE file for macro definitions for Solaris OS build and distro specific package names
# you just specify a macro name like "openssl" and get depending on the OS the currently
# active pacakge name (new IPS based library/security/openssl or SXCE SUNWopenssl-libraries 
# or S10 SUNWopenssly<u|r|whattheheckitisnamed>
# second EXAMPLE SUNWncurses/SUNWncurses-devel and "ncurses" and library/ncurses



#already included before?
%if %{?packagenamemacros}
#we are already included
%else
%include packagenamemacros.inc
%endif

# help the demo: pkgtool --interactive prep base-specs/packagenamemacros.spec
Name: packagenamemacros

%description
Demo the packagenamemacros.inc use:

   pkgtool --interactive prep base-specs/packagenamemacros.spec


Demo packagenamemacros.inc in your own spec file:

Include this spec file by the "use" statement and do include include/packagenamemacros.inc into 
your own spec file.
  (remove the comment # signs)  
  (the include packagenamemacros.inc is always needed in your spec, the %use... and 
# %packagenamemacros.prep is only for demonstration)

Demo setup: Edit SFEyourspec.spec
#    #always do the include, this is the only line really required for normal operation
#    %include packagenamemacros.inc

#    #optional for demoing inside your spec file's prep section or elsewhere
#    %use packagenamemacros = packagenamemacros.spec

then call the demo osdistop.prep inside your regular prep section to see at pkgbuild runtime 
what the result of the includefile packagenamemacros.inc on your development machine running 
your spec file is.

#    #optional for demoing inside your spec file is the call to "%packagenamemacros.prep"
#    %prep    
#    %setup -q -n %name-%version    

#    %packagenamemacros.prep

then run "pkgtool --interactive prep SFEyourspec.spec" and watch the variabled your might use in %if statements or other spec files code. enjoy.

NOTE: replace in variable name all "-" with "_"   ("-" is not valid in a variable name)
NOTE: specify forward or reverse  SUNWopenssl -> SUNWopenssl or openssl or library/security/openssl
NOTE:                             openssl     -> SUNWopenssl or openssl or library/security/openssl
NOTE:                library/security/openssl -> SUNWopenssl or openssl or library/security/openssl

%prep
echo "
packagenamemacros: osbuild %{osbuild}
packagenamemacros: SXCE %{SXCE}
packagenamemacros: os2nnn %{os2nnn}
packagenamemacros: oi147    %{oi147}    experimental
packagenamemacros: os201005 %{os201005} not yet released, name might eventually change?
packagenamemacros: os201003 %{os201003} deprecared, this release name was never used, will be removed
packagenamemacros: os200906 %{os200906}
packagenamemacros: os200902 %{os200902}
packagenamemacros: os200811 %{os200811}
packagenamemacros: osdistrelnumber %{osdistrelnumber}
packagenamemacros: osdistrelname   %{osdistrelname}
packagenamemacros: osdet299999 %{osdet299999}
" >/dev/null


echo "
requesting package SUNWopenssl resolves on %{osdistrelname} build %{osbuild}:
  BuildRequires for SUNWopenssl is contained in  %{pnm_buildrequires_SUNWopenssl}
       Requires for SUNWopenssl is contained in  %{pnm_requires_SUNWopenssl}
" >/dev/null

echo "
requesting package openssl w/o the SUNW prefix in the name resolves on %{osdistrelname} build %{osbuild}:
  BuildRequires for openssl is contained in  %{pnm_buildrequires_openssl}
       Requires for openssl is contained in  %{pnm_requires_openssl}
" >/dev/null

echo "
requesting package library/security/openssl resolves on %{osdistrelname} build %{osbuild}:
  BuildRequires for library/security/openssl is contained in  %{pnm_buildrequires_library_security_openssl}
       Requires for library/security/openssl is contained in  %{pnm_requires_library_security_openssl}
" >/dev/null



echo "
requesting package SUNWncurses / SUNWncurses-devel resolves on %{osdistrelname} build %{osbuild}:
  BuildRequires for SUNWncurses-devel is contained in  %{pnm_buildrequires_SUNWncurses_devel}
       Requires for SUNWncurses is contained in  %{pnm_requires_SUNWncurses}
" >/dev/null

echo "
requesting package ncurses w/o the SUNW prefix in the name resolves on %{osdistrelname} build %{osbuild}:
  BuildRequires for ncurses is contained in  %{pnm_buildrequires_ncurses}
       Requires for ncurses is contained in  %{pnm_requires_ncurses}
" >/dev/null

echo "
requesting package library/ncurses resolves on %{osdistrelname} build %{osbuild}:
  BuildRequires for library/ncurses is contained in  %{pnm_buildrequires_library_ncurses}
       Requires for library/ncurses is contained in  %{pnm_requires_library_ncurses}
" >/dev/null



%changelog
* Sat Oct 20 2010 - Thomas Wagner
- add oi to the mix
* Jun  1 2010 - Thomas Wagner
- inital to demo the name resolution depending on the operatingsystem type / distribution currently running
