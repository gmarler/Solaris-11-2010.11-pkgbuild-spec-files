Name:        redshift
IPS_package_name: desktop/redshift
SUNW_Pkg:    SFEredshift
Summary:     redshift color temperature adjustment utility
Version:     1.2
Release:     1
License:     GPLv3
Source:      http://launchpad.net/redshift/trunk/%{version}/+download/redshift-%{version}.tar.bz2
Patch01:     redshift-01-signal.h.diff
#SUNW_Copyright: %{name}.copyright
BuildRoot:   %{_tmppath}/%{name}-%{version}-build
Requires: SUNWxorg-clientlibs
Requires: SUNWgtk2
Requires: SUNWPython26

%description
Redhift adjusts the color temperature of your screen according to your
surroundings. This may help your eyes hurt less if you are working in
front of the screen at night.

%prep
rm -rf %name-%version
mkdir -p %name-%version
%setup -q 
%patch1 -p1

%build
export CFLAGS="-O4"
export CC=gcc
./configure --prefix=%{_prefix}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT%{_libdir}/python2.6
mkdir -p vendor-packages
mv site-packages/gtk_redshift vendor-packages/
rmdir site-packages
rm vendor-packages/gtk_redshift/*.pyo

%clean
/bin/rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%attr (0755, root, other) %{_datadir}/icons
%attr (0755, root, other) %{_datadir}/locale
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python2.6/vendor-packages/gtk_redshift


%changelog
* Tue Apr 20 2010 - laca@opensolaris.org
- create