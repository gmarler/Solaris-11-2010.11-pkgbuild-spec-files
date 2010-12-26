#
# spec file for package SFEircii
#
# includes module(s): ircii
#
%include Solaris.inc

%define	src_ver 20060725
%define	src_name ircii
%define	src_url	ftp://ircii.warped.com/pub/ircII

Name:		SFEircii
Summary:	Popular Unix Irc client
Version:	%{src_ver}
License:	BSD
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		ircii-01-config.diff
Patch2:		ircii-02.cast.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This is a popular Internet Relay Chat (IRC) client. It is a program
used to connect to IRC servers around the globe so that the user can
``chat'' with others.

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --with-default-server="irc.freenode.net"
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/irc
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Fix %files.
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
