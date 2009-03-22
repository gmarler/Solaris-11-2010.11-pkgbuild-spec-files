#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define tarball_version 2.21-02-src

Name:                SFEwebalizer
Summary:             Web server log analysis program
Version:             2.21
Source:              ftp://ftp.mrunix.net/pub/webalizer/webalizer-%{tarball_version}.tar.bz2
URL:		     http://www.webalizer.org

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgd2
Requires: SUNWgd2
BuildRequires: SUNWlexpt
Requires: SUNWlexpt

# Guarantee X/freetype environment, concisely (hopefully):
BuildRequires: SUNWGtku
Requires: SUNWGtku
# The above causes many things to get pulled in
BuildRequires: SUNWxwplt 
Requires: SUNWxwplt 
# The above brings in many things, including SUNWxwice and SUNWzlib
BuildRequires: SUNWxwxft 
Requires: SUNWxwxft 
# The above also pulls in SUNWfreetype2

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n webalizer-%{version}-02

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-gd=/usr/include/gd2 

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -D webalizer   $RPM_BUILD_ROOT%{_bindir}/webalizer
install -D webalizer.1 $RPM_BUILD_ROOT%{_mandir}/man1/webalizer.1
install -D sample.conf $RPM_BUILD_ROOT%{_sysconfdir}/webalizer.conf.sample

cd $RPM_BUILD_ROOT%{_bindir}
ln -s webalizer webazolver

#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc README CHANGES COPYING Copyright DNS.README INSTALL README.FIRST
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/webalizer.conf.sample

%changelog
* Sun Mar 22 2009 - Thomas Wagner
- add %doc
* Mon Feb 02 2008 - Thomas Wagner
- bump to 2.21
- switch from SFEgd to SUNWgd2, add configure --with-gd
* Sat Mar 31 2007 - Thomas Wagner
- change Build-Requires to be SFEgd-devel
*
* Wed Dec 13 2006 - Eric Boutilier
- Initial spec
