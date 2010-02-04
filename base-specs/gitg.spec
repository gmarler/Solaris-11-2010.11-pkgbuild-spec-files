#
# spec file for package gitg
#
#

Name:         gitg
Version:      0.0.5
Release:      1
Summary:      gitg is a git repository viewer targeting GTK+/GNOME.

Group:        System/Applications
License:      GPL
URL:          http://trac.novowork.com/gitg/
Source:       http://trac.novowork.com/gitg/raw-attachment/wiki/Releases/%{name}-%{version}.tar.bz2
Patch1:       gitg-01-name.diff 
Patch2:       gitg-02-inline.diff 

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
libtoolize --force --automake

automake -a -f -c --gnu
autoconf
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            %gtk_doc_option \
            --disable-static

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Feb 04 2010 - jedy.wang@sun.com
- Initial spec
