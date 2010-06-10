#
# spec file for package libsasl2 
#
#
%include Solaris.inc

Name:            SFElibsasl2
Summary:         Cyrus SASL API implentation 
Version:         2.1.23
License:         Carnegie Mellon University
Group:           System Environment/Utils
URL:             http://cyrusimap.web.cmu.edu/downloads.html#sasl
Source:          ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-%{version}.tar.gz
SUNW_BaseDir:    %{_basedir}
buildRoot:       %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n cyrus-sasl-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
#export CC=/usr/sfw/bin/gcc

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/sasl2
%{_libdir}/sasl2/*
%dir %attr (0755,root,bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_basedir}/share
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Initial SFElibsasl2 spec file.

