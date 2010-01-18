#
# spec file for package enchant
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
# bugdb: bugzilla.abisource.com
#

%define OSR 5805:1.3.0

Name:     	enchant
License:	LGPL v2.1
Version: 	1.5.0
Release:	1
Vendor:		Sun Microsystems, Inc.
Distribution:	Java Desktop System
Copyright:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:         %{_datadir}/doc
Autoreqprov:    on
URL:		http://www.abisource.com/projects/enchant/
Source:		http://www.abisource.com/downloads/%{name}/%{version}/%{name}-%{version}.tar.gz
# date:2008-11-19 owner:jefftsai type:branding
Patch2:         enchant-02-build-request-dict.diff
# This patch is applied until zemberek-server is implemented.
# date:2009-01-14 owner:fujiwara type:feature bugster:6793551
Patch3:         enchant-03-zemberek-segv.diff
# date:2009-01-14 owner:fujiwara type:feature
Patch4:         enchant-04-ordering.diff
# date:2009-08-20 owner:wangke type:branding
Patch5:		enchant-05-build-ispell.diff
# date:2009-11-04 owner:hem type:bug bugster:6887232
# Patch from upstream bug 12305 to return Turkish as available
# dictionary only if Zemberek server is installed
# http://bugzilla.abisource.com/show_bug.cgi?id=12305 
Patch6:		enchant-06-zemberek-dict-only-if-installed.diff
Summary:	Generic spell checking library
Group:		Applications/Text

%description
Enchant is a generic spell checking library that presents an API/ABI to 
applications.

%files
%defattr(-, root, root)

%prep
%setup  -q -n %{name}-%{version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1


%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
aclocal 
autoconf
automake -a -c -f
export CPPFLAGS=`pkg-config --cflags-only-I libstdcxx4`

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags `pkg-config --cflags-only-other libstdcxx4`"
export LDFLAGS="%{_ldflags} `pkg-config --libs libstdcxx4`"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --bindir=%{_bindir} \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --infodir=%{_datadir}/info \
    --localstatedir=/var \
	--with-myspell-dir=/usr/share/spell/myspell \
	--disable-aspell \
    --disable-static

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jan 02 2010 - yuntong.jin@sun.com
- Init spec file 
