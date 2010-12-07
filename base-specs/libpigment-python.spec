#
# spec file for package pigment-python
#
# includes module(s): pigment-python
#
# Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner yippi
#
# bugdb: https://code.fluendo.com/pigment/trac/
#
%{?!pythonver:%define pythonver 2.6}
%define OSR 9492:0.3.6

Name:            pigment-python
Summary:         Python interfaces for pigment
Vendor:          fluendo.com
Version:         0.3.12
License:         LGPL v2.1
URL:             https://core.fluendo.com/pigment/trac
Source0:         http://elisa.fluendo.com/static/download/pigment/pigment-python-%{version}.tar.bz2
BuildRoot:       %{_tmppath}/%{name}-%{version}-build

%description
Python interfaces for pigment.  Pigment is a library designed to easily
build user interfaces with embedded multimedia. Its design allows to use
it on several platforms, thanks to a plugin system allowing to choose
the underlying graphical API. Pigment is the rendering engine of Elisa,
the Fluendo Media Center project.

%prep
%setup -q -n pigment-python-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PYTHON=/usr/bin/python%{pythonver}
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

rm -f $RPM_BUILD_ROOT/%{_libdir}/python%{pythonver}/vendor-packages/*.la

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README AUTHORS
%doc(bzip2) NEWS COPYING ChangeLog
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/_pgmgtkmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/_pgmmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/_pgmimagingmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/pgm
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/pigment-python

%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Migrate to SFE.
* Tue Oct 13 2009 - Brian Cameron  <brian.cameron@sun.com>
- Do not install .pyo files.
* Tue Nov 11 2008 Jerry Tan <jerry.tan@sun.com>
- Bump to 0.3.9
* Tue Sep 30 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.8.
* Wed Sep 17 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.7.
* Thu Sep 11 2008 Jerry Yu <jijun.yu@sun.com>
- Bump to 0.3.6.
* Thu Jul 31 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.5.
* Wed Jul 23 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.4.
* Wed Mar 19 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.3
* Wed Feb 06 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.2.
* Wed Jan 16 2008 Brian Cameron  <brian.cameron@sun.com>
- Created.
