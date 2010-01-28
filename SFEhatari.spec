#
# RPM spec file for Hatari
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	hatari

Name:		SFEhatari
URL:		http://hatari.berlios.de/
License:	GPLv2
Group:		System/Emulators/Other
Version:	1.3.1
Summary:	an Atari ST emulator suitable for playing games
Source:		http://download.berlios.de/%{src_name}/%{src_name}-%{version}.tar.bz2
Patch1:		hatari-01-scandir.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{src_name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWzlib
Requires: SUNWzlib
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl

%description
Hatari is an emulator for the Atari ST, STE, TT and Falcon computers.
The Atari ST was a 16/32 bit computer system which was first released by Atari
in 1985. Using the Motorola 68000 CPU, it was a very popular computer having
quite a lot of CPU power at that time.
Unlike many other Atari ST emulators which try to give you a good environment
for running GEM applications, Hatari tries to emulate the hardware of a ST as
close as possible so that it is able to run most of the old ST games and demos.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
export CC=/usr/sfw/bin/gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm -lsocket"
ksh ./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --sysconfdir=%{_sysconfdir}
gmake

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_mandir}/man1 && gunzip hatari.1.gz


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/hatari.1
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, sys) %{_datadir}/%{src_name}
%{_datadir}/%{src_name}/*
%dir %attr (0755, root, other) %{_docdir}
%dir %{_docdir}/%{src_name}
%_docdir/%{src_name}/*.txt
%_docdir/%{src_name}/*.html
%dir %_docdir/%{src_name}/images
%_docdir/%{src_name}/images/*.png

%changelog -n hatari
* Sun Jan 24 2010 - Milan Jurik
- conversion for SFE

* Sat Sep 05 2009 - Thomas Huth
- Hatari version 1.3.1

* Sun Aug 16 2009 - Thomas Huth
- Hatari version 1.3.0

* Sat Jan 24 2009 - Thomas Huth
- Hatari version 1.2.0

* Sat Nov 29 2008 - Thomas Huth
- Hatari version 1.1.0

* Wed Jan 02 2008 - Thomas Huth
- Adapted RPM to the latest source code level (aiming at version 1.0.0)

* Sun May 06 2007 - Thomas Huth
- Adapted spec file to be able to build Hatari with RedHat, too

* Sun Aug 27 2006 - Thomas Huth
- Upgraded to version 0.90

* Tue Oct 18 2005 - Thomas Huth
- initial package
