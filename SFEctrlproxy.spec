#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define SUNWglib2      %(/usr/bin/pkginfo -q SUNWglib2 && echo 1 || echo 0)

Name:                SFEctrlproxy
Summary:             ctrlproxy - Detachable IRC proxy
Version:             3.0.8
Source:              http://www.ctrlproxy.org/releases/ctrlproxy-%{version}.tar.gz
Patch1:              ctrlproxy-01-solaris.diff
Patch2:              ctrlproxy-02-sunpro.diff
Patch3:              ctrlproxy-03-daemon.diff
Patch4:              ctrlproxy-04-services.diff
Url:                 http://www.ctrlproxy.org/
License:             GPLv3
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWglib2
BuildRequires: SUNWglib2-devel
Requires: SUNWglib2
%else
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs-devel
%endif
BuildRequires: SUNWgnome-common-devel
Requires: SUNWgss
BuildRequires: SUNWgnutls-devel
Requires: SUNWgnutls
BuildRequires: SUNWlibgcrypt-devel
Requires: SUNWlibgcrypt
BuildRequires: SUNWlxsl

Requires: %name-root

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
%setup -q -n ctrlproxy-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./autogen.sh
./configure \
            --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
	    --docdir=%{_docdir} \
            --mandir=%{_mandir}

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/ctrlproxyd
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ctrlproxy
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/ctrlproxy
%{_datadir}/ctrlproxy/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/ctrlproxy
%{_docdir}/ctrlproxy/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Tue Oct 15 2009 - trisk@opensolaris.org
- Add patch3.
- Add patch4. 
* Wed Oct 07 2009 - trisk@opensolaris.org
- Update dependencies.
- Add patch3.
* Mon Oct 05 2009 - trisk@opensolaris.org
- Initial spec.
