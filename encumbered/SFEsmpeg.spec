#
# spec file for package SFEsmpeg
#
# includes module(s): smpeg
#
%include Solaris.inc

%define src_name smpeg
%define src_url http://mirrors.dotsrc.org/lokigames/open-source

Summary:	SDL MPEG Library
Name:		SFEsmpeg
Version:	0.4.4
Copyright:	LGPL
Group:		System Environment/Libraries
Source:		%{src_url}/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		smpeg-01-sunstudio.diff
URL:		http://www.lokigames.com/development/smpeg.php3
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder
and SPLAY, an mpeg audio decoder created by Woo-jae Jung. We have
completed the initial work to wed these two projects in order to 
create a general purpose MPEG video/audio player for the Linux OS. 

%package devel
Summary: Libraries, includes and more to develop SMPEG applications.
Group: Development/Libraries
Requires: %{name}

%description devel
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder
and SPLAY, an mpeg audio decoder created by Woo-jae Jung. We have
completed the initial work to wed these two projects in order to 
create a general purpose MPEG video/audio player for the Linux OS. 

This is the libraries, include files and other resources you can use
to develop SMPEG applications.

%prep
rm -rf ${RPM_BUILD_ROOT}

%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="%{_ldflags} -lnsl -lsocket"
export CFLAGS="%{optflags}"
./configure --prefix=%{_prefix} --disable-gtk-player --disable-debug --disable-opengl-player --enable-static=no
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{_prefix} install
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_datadir}
rm $RPM_BUILD_ROOT%{_mandir}/man1/gtv.1
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc CHANGES COPYING README
%{_bindir}/plaympeg
%{_libdir}/lib*.so.*
%dir %attr (0755, root,sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/*

%files devel
%defattr(-, root, bin)
%doc CHANGES COPYING README
%{_bindir}/smpeg-config
%{_prefix}/include/*
%{_libdir}/lib*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Sun May 10 2010 - Milan Jurik
- initial import to SFE
* Fri Mar  3 2000 Sam Lantinga <hercules@lokigames.com>
- Split package into development and runtime packages
