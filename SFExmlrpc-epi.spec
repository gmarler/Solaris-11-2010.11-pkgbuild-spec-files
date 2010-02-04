#
# spec file for package SFExmlrpc-epi
#
# includes module(s): xmlrpc-epi
#
%include Solaris.inc

%include base.inc

%use xmlrpc_epi = xmlrpc-epi.spec

Name:                   SFExmlrpc-epi
Summary:                A general purpose implementation of the xmlrpc specification in C
Group:                  System/Libraries
Version:                %{xmlrpc_epi.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%xmlrpc_epi.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags"
export CFLAGS_PERSONAL="%optflags"
export LDFLAGS="%_ldflags"
%xmlrpc_epi.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%xmlrpc_epi.install -d %name-%version
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Jan 29 2010 - brian.cameron@sun.com
- Initial spec.
