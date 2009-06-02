#
# spec file for package SFEmp3c
#

%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/sfw/bin/g++
%include base.inc


Name:                    SFEmp3c
Summary:                 mp3c - ripp audio cd
URL:                     http://wspse.de/WSPse/Linux-MP3c.php3
Version:                 0.31
Source:                  ftp://ftp.wspse.de/pub/linux/wspse/mp3c-%{version}.tar.bz2


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc

BuildRequires: SUNWncurses-devel
Requires: SUNWncurses


%prep
%setup -q -n mp3c-%version

%build

export CC=gcc
export CXX=g++

#export CFLAGS="%optflags -I/usr/gnu/include/ncurses -DHAVE_LINUX_CDROM_H"
#export CXXFLAGS="%cxx_optflags -I/usr/gnu/include/ncurses -DHAVE_LINUX_CDROM_H"

export CFLAGS="%optflags -I/usr/include/ncurses -DHAVE_SYS_CDIO_H"
export CXXFLAGS="%cxx_optflags -I/usr/include/ncurses -DHAVE_SYS_CDIO_H"
export LDFLAGS="%_ldflags"



./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Mon Feb 23 2009  - Thomas Wagner
- Initial spec
