#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_version  2.03

Name:                SFElzo
Summary:             Lossless data compression library
Version:             2.3
Source:              http://www.oberhumer.com/opensource/lzo/download/lzo-%{src_version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{src_version}-build
%include default-depend.inc

%prep
%setup -q -n lzo-%src_version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no \
            --enable-shared=yes

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/liblzo2.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon 29 2010 - Milan Jurik
- update to 2.03
*  Mars 25 2010 - Gilles Dauphin
- IPS compat versioning
* Wed Wep 27 2006 - Eric Boutilier
- Initial spec
