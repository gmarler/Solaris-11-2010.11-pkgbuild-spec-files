#
# spec file for package SFEwesnoth.spec
#
%include Solaris.inc

# For binary packages on wesnoth.org
#%define _basedir /opt/games

%define wesnoth_datadir %{_datadir}/wesnoth

# Relative path on prefix 
%define pythonlibdir lib/python2.4/site-packages/wesnoth
%define abs_pythonlibdir %{_basedir}/%{pythonlibdir}

%define src_version 1.6.5

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    	SFEwesnoth
Summary:                 	Battle for Wesnoth is a fantasy turn-based strategy game
Version:                 	1.6.5
License:			GPLv2
URL:				http://www.wesnoth.org
Meta(info.upstream):            David White
Meta(info.repository_url):      http://svn.gna.org/svn/wesnoth 
Meta(pkg.detailed_url):         http://www.wesnoth.org
Meta(info.maintainer):		Petr Sobotka sobotkap@gmail.com
SUNW_Copyright:			wesnoth.copyright
Source:                  	%{sf_download}/wesnoth/wesnoth-%{src_version}.tar.bz2
Patch2:			        wesnoth-02-fixusleep.diff
Patch3:			        wesnoth-03-fixtolower.diff
Patch4:			        wesnoth-04-fixatoi.diff
Patch5:			        wesnoth-05-fixround.diff
Patch6: 		        wesnoth-06-fixreturn.diff
Patch8:			        wesnoth-08-fixscons.diff
Patch9:			        wesnoth-09-fixrand.diff
Patch10:		        wesnoth-10-fixstd.diff

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
BuildRequires:		SFEscons
BuildRequires:          SUNWgnome-common-devel
BuildRequires:          SUNWgnu-gettext
Requires:	        SFEsdl-mixer
Requires:	        SFEsdl-ttf
Requires:	        SFEsdl-net
Requires:	        SFEsdl-image
Requires:   	        SFEboost
Requires:	        SUNWPython
SUNW_BaseDir:     /

#%package server
#Summary:					Deamon to run Wesnoth game server
#Requires:					SFEboost

%prep
%setup -q -n wesnoth-%{src_version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export MSGFMT=/usr/gnu/bin/msgfmt

scons -j $CPUS default_targets=wesnoth prefix=%{_basedir} 	\
	python_site_packages_dir=%{pythonlibdir}

%install
rm -Rf $RPM_BUILD_ROOT/*

scons install prefix=%{_basedir} python_site_packages_dir=%{pythonlibdir} \
	mandir=%{_mandir} destdir=$RPM_BUILD_ROOT

scons install-pytools prefix=%{_basedir} 		\
	python_site_packages_dir=%{pythonlibdir} destdir=$RPM_BUILD_ROOT

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wesnoth
%{_bindir}/wml*
%{_bindir}/wesnoth_addon_manager
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%defattr (-, root, other)
%dir %attr (0755, root, other) %{wesnoth_datadir}
%{wesnoth_datadir}/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/wesnoth
%{_docdir}/wesnoth/*
%dir %attr (0755, root, other) %{abs_pythonlibdir}
%{abs_pythonlibdir}/*

#%files server
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/wesnothd
#%dir %attr (0750, root, other) /var/run/wesnothd

%changelog
* Sat Sep 12 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to version 1.6.5
* Fri Aug 07 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to version 1.6.4
* Sat Apr 18 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to 1.6.1 (merged from SFEwesnoth-dev)
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
