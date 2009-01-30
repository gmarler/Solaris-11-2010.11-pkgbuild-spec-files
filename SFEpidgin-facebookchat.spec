#
# spec file for package SFEpidgin-facebookchat
#

%include Solaris.inc

Name:                    SFEpidgin-facebookchat
Summary:                 Facebook chat plugin for pidgin
Group:                   System/GUI/GNOME
Version:                 1.47
Source:                  http://pidgin-facebookchat.googlecode.com/files/pidgin-facebookchat-source-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}_%{version}-build
%include default-depend.inc

Requires:    SUNWgnome-libs
Requires:    SUNWgnome-im-client
BuildRequires:    SUNWgnome-common-devel
BuildRequires:    SUNWgnome-im-client

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

$CC $CFLAGS $GLIB_CFLAGS $LIBPURPLE_CFLAGS *.c -o libfacebook.so $LDFLAGS $GLIB_LIBS $LIBPURPLE_LIBS

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
* Fri Jan 30 2009 - Albert Lee <trisk@acm.jhu.edu>
- Initial spec
