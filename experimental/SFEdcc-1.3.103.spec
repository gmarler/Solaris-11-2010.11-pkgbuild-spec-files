#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEdcc
Summary:             Distributed Checksum Clearinghouse
Version:             1.3.103
Source:              http://www.rhyolite.com/anti-spam/dcc/source/dcc-%{version}.tar.Z
#SUNW_BaseDir:        %{_basedir}
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Patch1:			dcc-01-install-sh.diff
Patch2:			dcc-02b-install-dont_set-user-group.diff
Patch3:			dcc-03b-remove-chown.diff
%include default-depend.inc

SUNW_Pkg_ThisZone:      true

#Requires: packagename

%prep
%setup -q -n dcc-%version
chmod -R +w *
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --with-installroot=$RPM_BUILD_ROOT \
            --homedir=%{_localstatedir}/dcc  \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
		--disable-chown

#unused --homedir=%{_prefix}/dcc  \

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/dcc
#I hate doing such:
%{_localstatedir}/dcc/[A-c]*
%{_localstatedir}/dcc/[e-z]*
#%class(CONFIG.prsv) %{_localstatedir}/dcc/dcc_conf
#%class(renamenew) %{_localstatedir}/dcc/dcc_conf
%class(preserve) %{_localstatedir}/dcc/dcc_conf

%changelog
* Sun Mai 03 2009 - Thomas Wagner
- bump to 1.3.103
* Fri 22 Aug 2008 - Thomas Wagner
- bump to 1.3.92
- reworked TODO
- reworked Patch3 dcc-03b-remove-chown.diff
* Thu 17 Jan 2007 - Thomas Wagner
- bump to 1.5.80, rework patches dcc-02* and dcc-03*
- adjust --homedir to be /var/dcc - TODO relocate the binaries/config out of /var/dcc into /usr/dcc and dcc_conf into /etc - mark dcc_conf volatile
- i.renamenew would be nicer, but it's not standard as i.preserve is (see: /usr/sadm/install/scripts/i.preserve)
* Tue 26 Jun 2007 - Thomas Wagner
- bump to 1.3.80
* Tue 26 Jun 2007 - Thomas Wagner
- bump to 1.3.57
* Sat 17 Feb 2007 - Thomas Wagner
- Initial spec
