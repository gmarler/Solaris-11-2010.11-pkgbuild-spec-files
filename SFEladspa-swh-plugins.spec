#
# spec file for package SFEladspa-swh-plugins
#
# includes module(s): swh-plugins
#

%include Solaris.inc
Name:                    SFEladspa-swh-plugins
Summary:                 LADSPA SWH plugins
URL:                     http://plugin.org.uk/
Version:                 0.4.15
Source:                  http://plugin.org.uk/releases/%{version}/swh-plugins-%{version}.tar.gz
Patch1:                  swh-plugins-01-nowall.diff
Patch2:                  swh-plugins-02-fixinline.diff
Patch3:			 swh-plugins-03-locale.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SFEladspa-devel
Requires: SFEladspa
BuildRequires: SUNWfftw3
Requires: SUNWfftw3

%prep
%setup -q -n swh-plugins-%version

%patch1 -p1
%patch2 -p1
%patch3 -p1

touch NEWS README AUTHORS ChangeLog COPYING

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ."
export CFLAGS="%optflags"
#export CXXFLAGS="%cxx_optflags -lCrun -lCstd"
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"

libtoolize -f -c
aclocal $ACLOCAL_FLAGS -I .
autoconf -f
autoheader
automake -a -c -f

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --datadir=%{_datadir}       \
            --libdir=%{_libdir}         \
            --mandir=%{_mandir} 

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %dir %{_libdir}/ladspa
%{_libdir}/ladspa/*.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %dir %{_datadir}/ladspa
%{_datadir}/ladspa/*
%dir %attr (0755, root, other) %dir %{_datadir}/locale
%dir %attr (0755, root, other) %dir %{_datadir}/locale/en_GB
%dir %attr (0755, root, other) %dir %{_datadir}/locale/en_GB/LC_MESSAGES
%{_datadir}/locale/en_GB/LC_MESSAGES/*

%changelog
* Thu Sep 18 2008 - jijun.yu@sun.com
- Add patch -03-locale.diff.
- Add files to %files.
* Mon Mar 17 2008 - brian.cameron@sun.com
- Created with version 0.4.15
