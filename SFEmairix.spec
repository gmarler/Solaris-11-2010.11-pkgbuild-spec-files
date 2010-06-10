#
# spec file for package SFEmairix
#
%include Solaris.inc

Name:            SFEmairix
Version:         0.22
Summary:         mairix is a program for indexing and searching email messages stored in maildir, MH or mbox folders.
License:         GPLv2
Group:           System Environment/Utils
URL:             http://www.rpcurnow.force9.co.uk/mairix/
Source:          http://downloads.sourceforge.net/mairix/mairix/mairix-%{version}.tar.gz


SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%description
mairix is a program for indexing and searching email messages stored in maildir, MH or mbox folders.

%prep
%setup -q -n mairix-%{version}


%build

./configure --prefix=%{_prefix} \
    --bindir=%{_bindir}	\
    --mandir=%{_mandir}	\
    --docdir=%{_datadir}

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rmdir $RPM_BUILD_ROOT/usr/local

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
#%{_docdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mairix
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/mairix.1
%{_mandir}/man5/mairixrc.5
%doc README
%doc dotmairixrc.eg


%changelog
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Initial SFEmairix spec file.
