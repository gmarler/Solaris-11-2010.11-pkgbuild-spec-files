#
# spec file for package SFEimapsync
#
# includes module(s): imapsync
#
%include Solaris.inc

%define perl_version 5.8.4

Name:		SFEimapsync
Summary:	Tool to migrate email between IMAP servers
Version:	1.344
License:	WTFPL
Group:		Applications/Internet
URL:		http://freshmeat.net/projects/imapsync/
Source:		http://www.linux-france.org/prj/imapsync/dist/imapsync-%{version}.tgz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWperl584core
Requires:	SUNWperl584core
BuildRequires:	SFEperl-mail-imapclient
Requires:	SFEperl-mail-imapclient
BuildRequires:	SFEperl-term-readkey
Requires:	SFEperl-term-readkey
BuildRequires:	SFEperl-io-socket-ssl
Requires:	SFEperl-io-socket-ssl
BuildRequires:	SFEperl-date-manip
Requires:	SFEperl-date-manip


%description
imapsync is a tool for facilitating incremental recursive IMAP
transfers from one mailbox to another. It is useful for mailbox migration,
and reduces the amount of data transferred by only copying messages that
are not present on both servers. Read, unread, and deleted flags are preserved,
and the process can be stopped and resumed. The original messages can
optionally be deleted after a successful transfer.

%prep
%setup -q -n imapsync-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT

export PATH=$PATH:/usr/perl5/bin
make install DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc ChangeLog CREDITS INSTALL TODO README FAQ
%{_bindir}/imapsync
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%attr(644, root, root) %{_mandir}/man1/imapsync.1*

%changeLog
* Thu Sep 02 2010 - Milan Jurik
- Initial spec based on Fedora
