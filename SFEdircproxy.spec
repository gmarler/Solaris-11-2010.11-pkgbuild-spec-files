#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name dircproxy
%define src_version 1.2.0-RC1

Name:                SFEdircproxy
Summary:             dircproxy - IRC proxy server
Version:             1.1.99.1
License:             GPLv2
Source:              http://dircproxy.googlecode.com/files/%{src_name}-%{src_version}.tar.gz
URL:                 http://code.google.com/p/dircproxy/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{src_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

aclocal
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir}	\
            --bindir=%{_bindir}		\
	    --datadir=%{_datadir}	\
	    --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_docdir}/dircproxy
mv $RPM_BUILD_ROOT%{_datadir}/dircproxy/* $RPM_BUILD_ROOT%{_docdir}/dircproxy
rmdir $RPM_BUILD_ROOT%{_datadir}/dircproxy

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc AUTHORS COPYING INSTALL HACKING README README.*  RELEASING FAQ NEWS TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/dircproxy
%{_docdir}/dircproxy/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue Apr 20 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
