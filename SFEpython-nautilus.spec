#
# spec file for package SFEpython-nautilus
#
# includes module(s): python-nautilus
#

%include Solaris.inc
Name:                    SFEpython-nautilus
Summary:                 Python binding for Nautilus
URL:                     http://svn.gnome.org/viewvc/nautilus-python/
Version:                 0.5.1
License:                 GPL
Source:                  http://ftp.gnome.org/pub/GNOME/sources/nautilus-python/0.5/nautilus-python-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%prep
%setup -q -n nautilus-python-%version

%build
PUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


./configure --prefix=%{_prefix}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/nautilus-python/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/nautilus/*
%{_libdir}/nautilus-python/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sat Mar 28 2009 - alfred.peng@sun.com
- Created
