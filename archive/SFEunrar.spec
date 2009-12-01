#
# spec file for package SFEunrar
#
# includes module(s): unrar
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use unrar64 = unrar.spec
%endif

%include base.inc
%use unrar = unrar.spec

Name:                    SFEunrar
Summary:                 %{unrar.summary}
Version:                 %{unrar.version}
URL:                     http://www.rarlab.com/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWlibms

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%unrar64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%unrar.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%unrar64.build -d %name-%version/%_arch64
%endif

%unrar.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%unrar64.install -d %name-%version/%_arch64
%endif

%unrar.install -d %name-%version/%{base_arch}
%if %can_isaexec
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
for i in unrar
do
  mv $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
  (
    cd $RPM_BUILD_ROOT%{_bindir}
    ln -s ../lib/isaexec $i
  )
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}
%hard %{_bindir}/unrar
%else
%{_bindir}/unrar
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/unrar
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%changelog
* Wed Aug 15 2007 - dougs@truemail.co.th
- Converted to 64bit
* Thu Jun 22 2006 - laca@sun.com
- rename to SFEunrar
- add missing deps
- move to /usr/bin
* Fri May 12 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
