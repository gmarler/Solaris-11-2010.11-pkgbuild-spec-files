#
# spec file for package SFEjhead
#
%include Solaris.inc

Name:            SFEjhead
Version:         2.90
Summary:         Tool for handling EXIF metadata in JPEG image files
License:         Public Domain
Group:           System Environment/Libraries
URL:             http://www.sentex.net/~mwandel/jhead/
Source:          http://www.sentex.net/~mwandel/jhead/jhead-%{version}.tar.gz


SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%description
Jhead is a tool for displaying and manipulating non-image portions of 
EXIF format JPEG image files, as produced by most digital cameras.


%prep
%setup -q -n jhead-%{version}


%build
export CC=gcc
make

%install
install -Dp -m0755 jhead $RPM_BUILD_ROOT%{_bindir}/jhead
install -Dp -m0755 jhead.1 $RPM_BUILD_ROOT%{_mandir}/man1/jhead.1
#in case old pkgbuild does not automaticly place %doc files there
#test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}
#mkdir $RPM_BUILD_ROOT%{_docdir}
#chmod 755 $RPM_BUILD_ROOT%{_docdir}
#chown root:other $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/doc
#%doc changes.txt readme.txt usage.html
#%dir %attr (0755, root, other) %{_docdir}
#%{_docdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/jhead
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/jhead.1

%changelog
* Mar 16 2010 - Gilles Dauphin
- bump release
* Wed Sep 10 2008 - pradhap (at) gmail.com
- doc file attribute set to root,other
* Wed Sep 10 2008 - pradhap (at) gmail.com
- Initial SFEjhead spec file.
