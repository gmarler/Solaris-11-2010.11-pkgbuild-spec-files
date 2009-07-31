#
# spec file for package SFExautolock
#
# includes module(s): xautolock
#

%include Solaris.inc
Name:                    SFExautolock
Summary:                 Launches a program if console is inactive for a time
URL:                     http://freshmeat.net/projects/xautolock/
Version:                 2.2
Source:                  http://www.ibiblio.org/pub/Linux/X11/screensavers/xautolock-%{version}.tgz
Patch1:                  xautolock-01-manpath.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n xautolock-%version

%build
export PATH=$PATH:/usr/X11/bin
xmkmf

# Need to patch the generated makefile to install manpages to the right
# location.  Perhaps there is a better way to do this?  Is this a bug in
# xmkmf?
#
%patch1 -p1

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

export MANPATH=/usr/X11/share/man
make install.man DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/bin
%{_prefix}/X11/bin/*
%dir %attr (0755, root, bin) %{_prefix}/X11/share
%dir %attr (0755, root, bin) %{_prefix}/X11/share/man
%dir %attr (0755, root, bin) %{_prefix}/X11/share/man/man1
%{_prefix}/X11/share/man/man1/*

%changelog
* Fri Jul 31 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created based on version 2.2
