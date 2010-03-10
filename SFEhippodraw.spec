#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
%include Solaris.inc

%define cc_is_gcc 1
%define pythonver 2.6
%include base.inc

Name:                SFEhippodraw
Summary:             Highly interactive data analysis environment
URL:                 http://www.slac.stanford.edu/grp/ek/hippodraw/
Version:             1.21.3
Source:              ftp://ftp.slac.stanford.edu/users/pfkeb/hippodraw/HippoDraw-%{version}.tar.gz
Patch1:              hippodraw-01-solaris.diff
Patch2:              hippodraw-02-numpy.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEboost-gpp
Requires: SFEqt
BuildRequires: SFEboost-gpp-devel
BuildRequires: SFEqt-devel
BuildRequires: SUNWdoxygen

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n HippoDraw-%version
%patch1 -p1
%patch2 -p1

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%{_ldflags} -L%{_cxx_libdir} -R%{_cxx_libdir}"

export PYTHON=/usr/bin/python%{pythonver}

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

aclocal $ACLOCAL_FLAGS -I config/m4
autoheader
automake -a -c -f
autoconf
echo yes | ./configure -prefix %{_prefix} \
           -sysconfdir %{_sysconfdir} \
           --enable-numpybuild \
           --enable-boostbuild \
           --with-boost-lib=/usr/lib/g++/3.4.3 \
           --with-boost-include=/usr/sfw/include/c++/3.4.3 \
           --with-boost-libname=boost_python

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/python%{pythonver}/vendor-packages/HippoDraw
%{_libdir}/python%{pythonver}/vendor-packages/hippo.pth
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/HippoDraw
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/HippoDraw-%{version}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/HippoDraw
%{_includedir}/HippoDraw/*

%changelog
* Mon Jul 09 2009 - Brian Cameron  <brian.cameron@sun.com>
- Initial spec based on 1.21.3.
