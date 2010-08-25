#
# spec file for package SFEofflineimap
#
# includes module(s): offlineimap
#
%include Solaris.inc

Name:		SFEofflineimap
Summary:	Bi-directional sync'ing of IMAP/Maildir email boxes
Version:	6.2.0.2
Group:		Applications/Internet
#Source:	http://github.com/jgoerzen/offlineimap/tarball/debian/%{version}
Source:		http://ftp.de.debian.org/debian/pool/main/o/offlineimap/offlineimap_%{version}.orig.tar.gz
URL:		http://wiki.github.com/jgoerzen/offlineimap/
License:	GPLv2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWPython

%prep
%setup -q -n offlineimap-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Wed Aug 25 2010 - Milan Jurik
- bump to 6.2.0.2 
* Sat Mar 31 2007 - Eric Boutilier
- Initial spec
- Python App: Two-way sync of IMAP/Maildir email boxes
