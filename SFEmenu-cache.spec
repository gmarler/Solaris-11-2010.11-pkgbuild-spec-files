#
# spec file for package SFEmenu-cache
#
# includes module(s): menu-cache
#
%include Solaris.inc

Name:                    SFEmenu-cache
Summary:                 LXDE menu cache
Version:                 0.2.5
Source:                  http://downloads.sourceforge.net/lxde/menu-cache-%{version}.tar.gz
URL:                     http://sourceforge.net/projects/lxde/

# owner:alfred date:2009-03-13 type:bug
Patch1:                  menu-cache-01-Werror.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n menu-cache-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lsocket"

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir} --libexecdir=%{_libexecdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/%{_libdir}/*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/menu-cached
%{_libdir}/menu-cache-gen
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.2.5.
* Tue Jul 28 2009 - alfred.peng@sun.com
- Bump to 0.2.4
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version
