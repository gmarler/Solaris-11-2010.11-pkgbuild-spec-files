#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
# bugdb: http://trac.filezilla-project.org/wiki
#

%define version_str 3.2.4.1_src
Name:		filezilla
Summary:	FileZilla FTP client
Version:	3.2.4.1
License:	GPL
URL:		http://filezilla.sourceforge.net/
Source:	    http://superb-east.dl.sourceforge.net/sourceforge/filezilla/FileZilla_%{version_str}.tar.bz2
# date:2008-03-06 owner:halton type:bug bugid:3424
Patch1:     %{name}-01-msgfmt.diff
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FileZilla is a fast and reliable FTP client and server with lots of
useful features and an intuitive interface.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

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

./autogen.sh
./configure  --prefix=%{_prefix}     \
			--libdir=%{_libdir}     \
			--libexecdir=%{_libexecdir} \
			--datadir=%{_datadir}       \
			--mandir=%{_mandir}     \
			--sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS docs/todo.txt
%attr(755,root,root) %{_bindir}/filezilla
%attr(755,root,root) %{_bindir}/fzsftp
%dir %{_datadir}/filezilla
%{_datadir}/filezilla/resources


%changelog
* Tue Jun 02 2009 - alfred.peng@sun.com
- Bump to 3.2.4.1.
* Thu Feb 05 2009 - alfred.peng@sun.com
- Bump to 3.2.0.
* Tue Dec 30 2008 - alfred.peng@sun.com
- Bump to 3.1.6.
  Remove two upstreamed patches: configure-in.diff and dirent-to-stat.diff.
* Wed Sep 24 2008 - alfred.peng@sun.com
- Bump to 3.1.3.
  Add two patches: multimap-const.diff and dirent-to-stat.diff.
* Fri Aug 29 2008 - alfred.peng@sun.com
- Bump to 3.1.1.
- Remove upstreamed patches: iter++.diff, SetActive.diff and locale.diff.
* Thu Mar 06 2008 - nonsea@users.sourceforge.net
- Bump to 3.0.7.1.
- Remove upstreamed patches: autogen.diff, vector-begin.diff,
  strrchr.diff, socket.diff, po-error.diff and vector-begin-more.diff
- Add patches iter++.diff, SetActive.diff, msgfmt.diff and locale.diff
* Mon Aug 06 2006 - nonsea@users.sourceforge.net
- Initial version
