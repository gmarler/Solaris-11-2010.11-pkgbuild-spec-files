#
# spec file for package gtkimageview
#
#

Name:         gtkimageview
Version:      1.6.4
Release:      1
Summary:      Image metadata library

Group:        System/Libraries
License:      LGPL
URL:          http://trac.bjourne.webfactional.com
Source:       http://trac.bjourne.webfactional.com/chrome/common/releases//%{name}-%{version}.tar.gz
Patch1:       gtkimageview-01-cflags.diff 
Patch2:       gtkimageview-02-void.diff 

BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Libnotify is a notification system for the GNOME desktop environment.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%ifos linux
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

aclocal $ACLOCAL_FLAGS
glib-gettextize --force --copy
intltoolize --force --automake
gtkdocize

automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --enable-compile-warnings=no \
            %gtk_doc_option \
            --disable-static

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Jan 22 2010 - jedy.wang@sun.com
- Initial spec
