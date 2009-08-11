#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEnetcat
Summary:             Read and write data across network connections
Version:             0.7.1
Source:              %{sf_download}/netcat/netcat-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n netcat-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# There's a man page, so omit the info files:
rm -r $RPM_BUILD_ROOT%{_prefix}/info

# The following is just a convenience symbolic link to netcat,
# and seems like not a good idea to put a two-letter
# command in /usr/bin unless there's a better reason
# than that:

rm $RPM_BUILD_ROOT%{_prefix}/bin/nc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/man/*
%dir %attr (0755, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/locale/it
%dir %attr (0755, root, other) %{_datadir}/locale/sk
%dir %attr (0755, root, other) %{_datadir}/locale/it/LC_MESSAGES
%dir %attr (0755, root, other) %{_datadir}/locale/sk/LC_MESSAGES
%{_datadir}/locale/it/LC_MESSAGES/*
%{_datadir}/locale/sk/LC_MESSAGES/*

%changelog
* Aug 2009 - Gilles Dauphin
- change %files
* Sat Sep 30 2006 - Eric Boutilier
- Initial spec
