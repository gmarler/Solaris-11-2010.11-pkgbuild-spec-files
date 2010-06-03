#
# spec file for package SFEsmf-grey.spec
#
# includes module(s): smf-grey
#
%include Solaris.inc
%include osdistro.inc

%define src_name	smf-grey

Name:		SFEsmf-grey
Summary:	Sendmail milter implementing greylisting
Version:	2.1.0
License:	GPLv2
Group:		System/Utilities
URL:		http://smfs.sourceforge.net/smf-grey.html
Source:		%{sf_download}/smfs/%{src_name}-%{version}.tar.gz
Source1:	smf-grey.xml
Patch1:		smf-grey-01-makefile.diff
Patch2:		smf-grey-02-init.diff
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#new os2nnn and starting with build 134
%if %{os2nnn}
%if %(expr %{osbuild} '>=' 134)
BuildRequires:	service/network/smtp/sendmail
%endif
%endif

#os os2nnn below build 134 (excluding)
%if %{os2nnn}
%if %(expr %{osbuild} '<' 134)
BuildRequires:	SUNWsndm
%endif
%endif

#SXCE
%if %SXCE
BuildRequires:	SUNWsndmu
%endif

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mail/smfs
install -c -m 644 smf-grey.conf $RPM_BUILD_ROOT%{_sysconfdir}/mail/smfs
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -c -m 755 smf-grey $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{src_name}
install -c -m 644 readme $RPM_BUILD_ROOT/%{_docdir}/%{src_name}
install -c -m 644 ChangeLog $RPM_BUILD_ROOT/%{_docdir}/%{src_name}
mkdir -p $RPM_BUILD_ROOT/lib/svc/method
install -c -m 755 init/smfgrey.solaris $RPM_BUILD_ROOT/lib/svc/method/smf-grey
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/%{src_name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/site/
install -c -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd smfs';
  echo '/usr/sbin/useradd -d %{_sysconfdir}/mail/smfs -s /bin/true -g smfs smfs';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel smfs';
  echo '/usr/sbin/groupdel smfs';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
group groupname="smfs"
user ftpuser=false gcos-field="smfs Reserved UID" username="smfs" password=NP group="smfs"

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_sbindir}
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, mail) %{_sysconfdir}/mail
%dir %attr (0755, root, sys) %{_sysconfdir}/mail/smfs
%{_sysconfdir}/mail/smfs/smf-grey.conf
/lib/svc/method/smf-grey
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/%{src_name}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/site
%class(manifest) %attr (0444, root, sys) %{_localstatedir}/svc/manifest/site/smf-grey.xml


%changelog
* Thu Jun 03 2010 - Milan Jurik
- Initial version
