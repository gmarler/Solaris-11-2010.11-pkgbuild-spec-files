#
# spec file for package SFEpidgin-facebookchat
#

%include Solaris.inc

Name:                    SFEpidgin-facebookchat
Summary:                 Facebook chat plugin for pidgin
Group:                   System/GUI/GNOME
Version:                 1.64
License:                 GPL v3
Source:                  http://pidgin-facebookchat.googlecode.com/files/pidgin-facebookchat-source-%{version}.tar.bz2
URL:                     http://code.google.com/p/pidgin-facebookchat/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

Requires:    SUNWgnome-libs
Requires:    SUNWgnome-im-client
Requires:    SFEjson-glib
BuildRequires:    SUNWgnome-common-devel
BuildRequires:    SUNWgnome-im-client
BuildRequires:    SFEjson-glib-devel

%prep
rm -rf %name_%version
%setup -q -n pidgin-facebookchat

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags" 
export LDFLAGS="%_ldflags -G"

GLIB_CFLAGS=$(pkg-config --cflags glib-2.0)
GLIB_LIBS=$(pkg-config --libs glib-2.0)
LIBPURPLE_CFLAGS=$(pkg-config --cflags purple)
LIBPURPLE_LIBS=$(pkg-config --libs purple)
JSON_GLIB_CFLAGS=$(pkg-config --cflags json-glib-1.0)
JSON_GLIB_LIBS=$(pkg-config --libs json-glib-1.0)

$CC $CFLAGS $GLIB_CFLAGS $LIBPURPLE_CFLAGS $JSON_GLIB_CFLAGS *.c -o libfacebook.so $LDFLAGS $GLIB_LIBS $LIBPURPLE_LIBS $JSON_GLIB_LIBS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/purple-2
cp libfacebook.so $RPM_BUILD_ROOT%{_libdir}/purple-2
for size in 16 22 48; do
	mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/pidgin/protocols/$size
	cp facebook${size}.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/pidgin/protocols/$size/facebook.png
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Wed Feb 03 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.64
* Sat Nov 14 2009 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.63
- Add license and URL
* Thu Jun 25 2009 - Albert Lee <trisk@forkgnu.org>
- Bump to 0.52
- Add SFEjson-glib dependency
* Fri Jan 30 2009 - Albert Lee <trisk@acm.jhu.edu>
- Initial spec
