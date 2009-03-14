#
# spec file for package SFEwesnoth.spec
#
%include Solaris.inc

# For binary packages on wesnoth.org
#%define _basedir /opt/games
#%define _bindir %{_basedir}/bin
#%define _datadir %{_basedir}/share
#%define _mandir %{_datadir}/man
#%define _libdir %{_basedir}/lib

%define _docdir %{_basedir}/share/doc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    	SFEwesnoth
Summary:                 	Battle for Wesnoth is a fantasy turn-based strategy game
Version:                 	1.4.7
Source:                  	%{sf_download}/wesnoth/wesnoth-%{version}.tar.bz2
#Patch1:                         wesnoth-01-fixheaders.diff
#Patch2:                         wesnoth-02-fixgccextension.diff
#Patch3:                         wesnoth-03-fixgccism.diff
Patch4:                         wesnoth-04-fixlocale.diff
Patch5:                         wesnoth-05-fixconfigure.diff
#Patch6:                         wesnoth-06-fixundefsymbol.diff
#Patch7:                         wesnoth-07-fixundef2.diff
#Patch8:                          wesnoth-08-fixconst.diff
Patch13:			wesnoth-13-fixconfigtest.diff
Patch14:			wesnoth-14-testboost.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires:		SFEsdl-mixer-devel
BuildRequires:		SFEsdl-ttf-devel
BuildRequires:		SFEsdl-net-devel
BuildRequires:		SFEsdl-image-devel
Requires:		SFEsdl-mixer
Requires:		SFEsdl-ttf
Requires:		SFEsdl-net
Requires:		SFEsdl-image
Requires:               SFEboost
Requires:		SUNWPython

%prep
%setup -q -n wesnoth-%version
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p1
#%patch7 -p1
#%patch8 -p1
%patch13 -p1
%patch14 -p1
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXXFLAGS="-O3 -library=stlport4 -staticlib=stlport4 -norunpath -features=tmplife -features=tmplrefstatic -features=extensions"
#export CXXFLAGS="%cxx_optflags"
#export LDFLAGS="%_ldflags -lsocket -lnsl"
export LDFLAGS="-library=stlport4 -staticlib=stlport4 -lsocket -lnsl -lboost_iostreams -L. -R."

# Cause configure script check for C compilers, but the build doesn't use any
#  of C compilers and cc doesn't eat -library=stlport4 and other options.
#  I defined cc as C++ compiler, until it will be fixed cleaner
export CC=$CXX
export CC32=$CXX32
export CC64=$CXX64

autoconf

export MSGFMT=/usr/gnu/bin/msgfmt
#export GMSGFMT=/usr/gnu/bin/msgfmt

./configure --prefix=%{_basedir}			\
            --bindir=%{_bindir}				\
            --datadir=%{_datadir}			\
            --mandir=%{_mandir}				\
            --libdir=%{_libdir}				\
            --htmldir=%{_docdir}			\
            --enable-editor                     	\
            --enable-shared			\
            --with-preferences-dir=".wesnoth" 	\
            --enable-python-install     \
    	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%defattr (-, root, other)
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/wesnoth
%{_datadir}/wesnoth/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/wesnoth
%{_docdir}/wesnoth/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages/wesnoth
%{_libdir}/python2.4/site-packages/wesnoth/*


%changelog
* Sat Mar 14 2009 - Milan Jurik
- Bump to 1.4.7
* Sun Oct 12 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.5
* Mon Jul 28 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.4
* Sun Jun 22 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.3 version
* Wed May 07 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.4.2 version
* Mon Mar 10 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.4 stable version.
- Changed preferences dir to ~/.wesnoth from ~/.wesnoth-dev which will 
	be used for development releases in future.
* Sun Feb 24 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.19 (last rc release before 1.4)
* Tue Feb 19 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.18
* Thu Feb 14 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.16
* Tue Jan 29 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.15
* Wed Jan 16 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.14
* Sat Jan 05 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Removed --enable-dummy-locales option from configure as it cause warning 
* Tue Jan 01 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.13
- Introduced new dependency SFEboost
- Changed compiler from gcc to sun studio + stlport4 (need to be same as for boost)
* Sat Dec 01 2007 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.12
* Mon Nov 19 2007 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.11
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Nov 11 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.10
* Fri Oct 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.9
- add html documentation
* Wed Sep 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.8
* Thu Sep 6 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
