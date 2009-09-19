#
# spec file for package SFEc-icap
#
# includes module(s): c-icap
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define	src_name c_icap
%define src_version 060708rc3

Name:                SFEc-icap
Summary:             An implementation of an ICAP server
Version:             0.060708.0.3
Source:              %{sf_download}/c-icap/%{src_name}-%{src_version}.tar.gz
Source1:             c-icap.xml
Patch1:              c-icap-01-chgrp.diff
Patch2:              c-icap-02-conf.diff 
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFEclamav-devel
Requires:	SFEclamav

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{src_version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --disable-static			\
	    --enable-shared			\
	    --enable-large-files		\
	    --enable-ipv6

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/var
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{src_name}/*.*a
install -d 0755 %{buildroot}%/var/svc/manifest/system/filesystem
install -m 0644 %{SOURCE1} %{buildroot}%/var/svc/manifest/system/filesystem

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/c_icap
%{_libdir}/c_icap/*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%dir %attr (0775, nobody, nobody) %{_localstatedir}/run/c-icap
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/system/filesystem/c-icap.xml

%changelog
* Sat Sep 19 2009 - Milan Jurik
- Initial spec
