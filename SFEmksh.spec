#
# spec file for package SFEmksh
#
# includes module(s): mksh
#
# Owner: lewellyn

# TODO: Find out how to force perl 5.8.4 to be used for build/test

%include Solaris.inc

%define arc4_version 1.27
%define mksh_version 39c
%define mksh_num_version 39.3
%define snap_version 20100108
# Requested by Thorsten Glaser:
# "R39 = 39.1, R39b = 39.2, etc. up to .8 and 39.9.yyyymmdd for snapshots"

Name:                SFEmksh
Summary:             The MirBSD Korn Shell R%{mksh_version}, an actively developed free implementation of the Korn Shell
Version:             %{mksh_num_version}
Source:              http://www.mirbsd.org/MirOS/dist/mir/mksh/mksh-R%{mksh_version}.cpio.gz
#Version:             %{mksh_num_version}.%{snap_version}
#Source:              http://www.freewrt.org/distfiles/mksh-%{snap_version}.cpio.gz
Source1:             http://www.mirbsd.org/MirOS/dist/hosted/other/arc4random.c.%{arc4_version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Group:               System/Shells
License:             Any permissive - MirOS Licence (BSD-alike)
URL:                 http://mirbsd.de/mksh
SUNW_Copyright:      %{name}.copyright

%include default-depend.inc
BuildRequires:       SUNWgzip
BuildRequires:       SUNWperl584core
# When 5.10 is used, SUNWperl510usr will also be required.
Requires:            %{name}-root

%description
mksh is the MirBSD enhanced version of the Public Domain Korn
shell (pdksh), a Bourne-compatible shell which is largely si-
milar to the original AT&T Korn shell; mksh is the only pdksh
derivate currently being actively developed.  It includes bug
fixes and feature improvements, in order to produce a modern,
robust shell good for interactive and especially script use.
mksh has UTF-8 support (in substring operations and the Emacs
editing mode) and, while R39a corresponds to OpenBSD 4.5-cur-
rent ksh (without GNU bash-like PS1 and fancy character clas-
ses), adheres to SUSv3 and is much more robust.  The code has
been cleaned up and simplified, bugs fixed, standards compli-
ance added, and several enhancements (for extended compatibi-
lity to other modern shells--as well as a couple of its own)
have been placed.

Authors:
--------
    Thorsten Glaser <tg@mirbsd.org>

%package root
Summary:             %{summary} - / filesystem
SUNW_BaseDir:        /
%include default-depend.inc
BuildRequires:       SUNWxcu4
Requires:            SUNWxcu4

%prep
rm -rf mksh-%{mksh_version}
%setup -q -T -c -n "mksh-%{mksh_version}"
gzip -dc "%{SOURCE0}" | cpio -mid
cp "%{SOURCE1}" mksh/arc4random.c

%build
export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags -xipo"
export RPM_OPT_FLAGS="$CFLAGS"

cd mksh
gzip -n9 <dot.mkshrc >dot.mkshrc.gz
sh Build.sh -r && test -f mksh

# run regression test
env PERL=/usr/perl5/perl5.8.4/bin/perl ./test.sh -v

%install
rm -rf "%{buildroot}"
install -d -m0755 "%{buildroot}%{_bindir}"
install -d -m0755 "%{buildroot}%{_mandir}/man1"
install -c -m0755 mksh/mksh "%{buildroot}%{_bindir}/mksh"
install -c -m0644 mksh/mksh.1 "%{buildroot}%{_mandir}/man1/mksh.1"
install -d -m0755 "%{buildroot}/etc/skel"
install -c -m0644 mksh/dot.mkshrc "%{buildroot}/etc/skel/.mkshrc"

%post root
if [ ! -s $BASEDIR/etc/shells ]; then
  echo "/bin/bash
/bin/csh
/bin/jsh
/bin/ksh
/bin/ksh93
/bin/pfcsh
/bin/pfksh
/bin/pfsh
/bin/sh
/bin/tcsh
/bin/zsh
/sbin/jsh
/sbin/sh
/usr/bin/bash
/usr/bin/csh
/usr/bin/jsh
/usr/bin/ksh
/usr/bin/ksh93
/usr/bin/pfcsh
/usr/bin/pfksh
/usr/bin/pfsh
/usr/bin/sh
/usr/bin/tcsh
/usr/bin/zsh
/usr/sfw/bin/zsh
/bin/mksh
/usr/bin/mksh" > $BASEDIR/etc/shells
  echo "Created $BASEDIR/etc/shells"
else
  /usr/xpg4/bin/grep -q "^/bin/mksh$" $BASEDIR/etc/shells || \
  echo "/bin/mksh" >> $BASEDIR/etc/shells
  /usr/xpg4/bin/grep -q "^/usr/bin/mksh$" $BASEDIR/etc/shells || \
  echo "/usr/bin/mksh" >> $BASEDIR/etc/shells
  echo "Updated $BASEDIR/etc/shells"
fi

%postun root
if [ ! -x $BASEDIR/usr/bin/mksh ]; then
  /usr/xpg4/bin/grep -vE "^/(usr/)?bin/mksh$"  $BASEDIR/etc/shells > $BASEDIR/etc/shells.pkg
  cat $BASEDIR/etc/shells.pkg > $BASEDIR/etc/shells && rm -f $BASEDIR/etc/shells.pkg
  echo "Elided $BASEDIR/etc/shells"
else
  echo "No changes made to $BASEDIR/etc/shells"
fi

%clean
rm -rf "%{buildroot}"

%files
%defattr (-, root, bin)
%doc mksh/dot.mkshrc.gz
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mksh
%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%doc %{_mandir}/man1/mksh.1*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) /etc
%dir %attr (0755, root, sys) /etc/skel
%config(noreplace) /etc/skel/.mkshrc

%changelog
* Tue Mar 02 2010 - matt@greenviolet.net
- Initial spec file
