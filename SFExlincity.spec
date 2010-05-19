#
# spec file for package SFExlincity
#

%include Solaris.inc

%define src_name lincity

Name:		SFExlincity
Summary:	xlincity - Simulation game based on opensourced components of S*mc*ty. 
Group:		Game/Simulation
URL:		http://lincity.sourceforge.net 
Version:	1.12.1
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz 
Patch1:		xlincity-01-solaris.diff
SUNW_Copyright:	%{name}.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q  -n %{src_name}-%{version} 
find ./intl -name \*.c -exec dos2unix {} {} \;
find ./intl -name \*.h -exec dos2unix {} {} \;
find ./intl -name \*.charset -exec dos2unix {} {} \;
%patch1 -p1

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*/LC_MESSAGES/%{src_name}.mo

%changelog
* Wed May 19 2010 - Milan Jurik
- update to 1.12.1
* Wed Jan 23 2008 - Brian Nitz - <brian dot nitz at sun dot com> 
- Initial version.
