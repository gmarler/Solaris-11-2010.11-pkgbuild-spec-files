#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibnet
Summary:             Packet Construction Library
Version:             1.1.2.1
Source:              http://download2us.softpedia.com/dl/d9db9a5960f231f8eb12d82e2848a28d/49956ff9/500010275/linux/libnet-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
%setup -q -n libnet

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=/usr/sfw/bin/gcc
# export CFLAGS="%optflags"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"

export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

# Following is a hack that comments out these lines in libnet_link_dlpi.c:
#
# if (*eos != '\0')
# {
#     snprintf(l->err_buf, LIBNET_ERRBUF_SIZE,
#             "%s(): %s bad unit number\n", __func__, l->device);
#     goto bad;
# }

perl -i.orig -lne 'print q!/*! if $.==142;print q!*/! if $.==148;print' src/libnet_link_dlpi.c

# It was done because a bug here makes libnet (and therefore ettercap)
# think that the e1000g0 interface on my laptop is invalid causing ettercap
# to fatally exit as a result. Beware: this means the intent for the ommited
# code is now being circumvented.

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# Because libnet appears incapable of producing a shared library,
# this spec file produces only a libnet-devel package
#
# %files
# ...

%files devel

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Feb 13 2009 - alfred.peng@sun.com
- Fix the broken download url
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Nov 05 2006 - Eric Boutilier
- Force gcc; create devel package
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
