#
# spec file for package SFEdictd
#
# includes module(s): dictd
#
%include Solaris.inc

Name:                    SFEdictd
Summary:                 Dictd Server and Client
Version:                 1.9.15
Source:                 ftp://ftp.dict.org/dict/dictd-%{version}.tar.gz
URL:                     http://dict.org
#SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu

%prep
%setup -q -n dictd-%version

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

gmake

%install
gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT/etc
echo "server dict.org" > /$RPM_BUILD_ROOT/etc/dict.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) /usr/sbin
/usr/sbin/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man8/*

%dir %attr (0755, root, bin) %{_libdir}

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Jun 19 2010 - pradhap (at) gmail.com
- Fixed URL
* Mar 29 2008 - pradhap (at) gmail.com
- Initial dictd spec file.

