#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define _prefix %{_basedir}/gnu

Name:                SFEfile
Summary:             determine file type
Version:             5.04
Source:              ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n file-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rmdir ${RPM_BUILD_ROOT}%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/misc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%dir %attr (0755, root, bin) %{_mandir}/man4
%{_mandir}/man4/*.4

%changelog
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Bump to 5.04
* Tue Oct 22 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 4.26
* Sat Jul 15 2007 - dougs@truemail.co.th
- Bump to 4.21
* Thu May 03 2007 - nonsea@users.sourceforge.net
- Bump to 4.20.
- Add patch file-01-REG_STARTEND.diff, get original copy from
  ftp://ftp.astron.com/pub/file/patch-4.20-REG_STARTEND
* Mon Jan 15 2007 - laca@sun.com
- bump to 4.19
* Tue Nov 07 2006 - Eric Boutilier
- Initial spec
