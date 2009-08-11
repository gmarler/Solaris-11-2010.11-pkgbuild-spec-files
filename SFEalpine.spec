# 
# 
# 
%include Solaris.inc

#%define tcl_version 8.4
#%define tcl_8_3 %(pkgchk -l SUNWTcl 2>/dev/null | grep /usr/sfw/bin/tclsh8.3 >/dev/null && echo 1 || echo 0)
%define SUNWgawk      %(/usr/bin/pkginfo -q SUNWgawk && echo 1 || echo 0)

Name:                SFEalpine
License:             Apache
Summary:             University of Washington Alpine mail user agent
Version:             2.00
Source:              ftp://ftp.cac.washington.edu/alpine/alpine-%{version}.tar.bz2
Patch2:              alpine-02-CC.diff
URL:                 http://www.washington.edu/alpine/
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
Group:		     Office/Email
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries
BuildRequires: SUNWhea
Requires: SUNWcsl
#BuildRequires: SUNWTcl
%if %SUNWgawk
BuildRequires: SUNWgawk
%else
BuildRequires: SFEgawk
%endif

%prep
%setup -q -n alpine-%{version}
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -mt %{sfw_lib_path}"

#%if %tcl_8_3
#TCL_OPTS="--with-tcl-lib=tcl8.3"
#%else
#TCL_OPTS="--with-tcl-lib=tcl%{tcl_version}"
#%endif
# Disable Tcl until we figure out what to do with Web Alpine
TCL_OPTS=--without-tcl

SSL_CERTS_DIR=/etc/sfw/openssl/certs
SSL_INCLUDE_DIR=%{sfw_inc}
SSL_LIB_DIR=/usr/sfw/lib
if [ ! -d "$SSL_INCLUDE_DIR/openssl" ]; then
	SSL_INCLUDE_DIR=/usr/include
fi

# autoconf

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
	    --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-system-pinerc=%{_sysconfdir}/pine.conf \
	    --with-system-fixed-pinerc=%{_sysconfdir}/pine.conf.fixed \
            --with-passfile=.pine-passfile \
            --disable-debug \
            --with-debug-level=0 \
	    --with-ssl-certs-dir=$SSL_CERTS_DIR \
	    --with-ssl-include-dir=$SSL_INCLUDE_DIR \
	    --with-ssl-lib-dir=$SSL_LIB_DIR \
            $TCL_OPTS

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

for prog in pico pilot rpdump rpload; do
	mv $RPM_BUILD_ROOT%{_bindir}/$prog $RPM_BUILD_ROOT%{_bindir}/alpine-$prog
	mv $RPM_BUILD_ROOT%{_mandir}/man1/$prog.1 $RPM_BUILD_ROOT%{_mandir}/man1/alpine-$prog.1
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Mon Aug 10 2009 - matt@greenviolet.net
- Allow BuildRequires to accept SUNWgawk
- Remove autoconf, as source is unfriendly to newer versions and aclocal doesn't help.
* Mon Mar 02 2009 - Albert Lee
- Fix SSL support
* Tue Oct 21 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Fix link
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add license and grouping
* Mon May 12 2008 - trisk@acm.jhu.edu
- Bump to 1.10
* Sat Jan 05 2007 - Thomas Wagner
- bump to 1.00 - old dwnl file removed, no other changes to spec/patches
* Fri Dec 07 2007 - trisk@acm.jhu.edu
- Bump to 0.999999 (Six Nines), drop patch1
* Fri Nov 09 2007 - trisk@acm.jhu.edu
- Bump to 0.99999, replace patch1
* Sat Oct 13 2007 - laca@sun.com
- add patch for using $CC instead of /opt/SUNWspro/bin/cc
* Mon Oct 08 2007 - trisk@acm.jhu.edu
- Initial spec, should be friendly with SFEpine
