#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# In a default configuration, non-root users can't run ettercap because
# they don't have priveleges to access the raw network interface (at least 
# that was my experience when I tested this).

%include Solaris.inc

Name:                SFEettercap
Summary:             MITM LAN attack prevention suite; includes graphical (gtk) support
Version:             0.7.3
Source:              %{sf_download}/ettercap/ettercap-NG-%{version}.tar.gz
Patch1:              patches/ettercap-NG-01-nogcc.diff
Patch2:              patches/ettercap-NG-02-debian-521857.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWxwinc
BuildRequires: SUNWncurses-devel
BuildRequires: SUNWlibpcap
BuildRequires: SUNWlibnet
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWzlib
BuildRequires: SUNWltdl
#
Requires: SUNWgtk2
Requires: SUNWxwplt
Requires: SUNWncurses
Requires: SUNWlibpcap
Requires: SUNWlibnet
Requires: SUNWopenssl-libraries
Requires: SUNWzlib
Requires: SUNWltdl
Requires: %name-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n ettercap-NG-%version
%patch1 -p1
%patch2 -p1
# fix struct initialisers
find  plug-ins -name '*.c' -exec perl -pi -e 's, (ettercap_version|name|info|version|init|fini): ( *),.\1 = \2,' {} ';'

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

autoconf
export CFLAGS="%optflags"
# Workaround for bad check in libnet/libnet-types.h: #if (__sun__ && __svr4__)
export CPPFLAGS="-I%{xorg_inc} -D__sun__=1 -D__svr4__=1"
export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path}"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir}	\
            --mandir=%{_mandir}		\
            --sysconfdir=%{_sysconfdir}	\
	    --enable-gtk

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Tue Jul 20 2010 - Albert Lee <trisk@opensolaris.org>
- Update dependencies
- Do not require gcc
- Add patch1, patch2
* Sat Apr 21 2007 - dougs@truemail.co.th
- Added %{_libdir} to %files
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Nov 05 2006 - Eric Boutilier
- Rename from ettercap-NG to ettercap; fix and adjust dependencies; force gcc
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
