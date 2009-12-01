#
# spec file for package SFExsane
#
# includes module(s): xsane
#
%include Solaris.inc
%use xsane = xsane.spec

Name:                    SFExsane
Summary:                 Graphical scanning frontend for the SANE scanner interface.
Group:                   Utility
Version:                 %{xsane.version}
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgnome-base-libs
BuildRequires:           SUNWgnome-base-libs-devel
Requires:                SFEsane-backends
BuildRequires:           SFEsane-backends-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%xsane.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
# /usr/sfw needed for libusb
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -L/usr/gnu/lib -R/usr/gnu/lib"
%xsane.build -d %name-%version
	    		
%install
rm -rf $RPM_BUILD_ROOT
%xsane.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

#Create a link to xsane binary for gimp plugin
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gimp/2.0/plug-ins
chmod -R 755 $RPM_BUILD_ROOT%{_libdir}/gimp
cd $RPM_BUILD_ROOT%{_libdir} & ln -s %{_bindir}/xsane $RPM_BUILD_ROOT%{_libdir}/gimp/2.0/plug-ins

%if %build_l10n
# Rename zh dir to zh_CN as zh is a symlink to zh_CN and causing installation
# problems as a dir.
cd $RPM_BUILD_ROOT%{_datadir}/locale
mv zh zh_CN
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/sane
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/gimp
%dir %attr (0755, root, bin) %{_libdir}/gimp/2.0
%dir %attr (0755, root, bin) %{_libdir}/gimp/2.0/plug-ins
%{_libdir}/gimp/2.0/plug-ins/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version numbers.
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to CFLAGS/LDFLAGS
* Mon Apr 02 2007 - daymobrew@users.sourceforge.net
- Rename zh dir to zh_CN in %install as zh a symlink to zh_CN and causing
  installation problems as a dir.
* Tue Mar 20 2007 - simon.zheng@sun.com
- Split into 2 files, SFExsane.spec and 
  linux-specs/xsane.spec.
* Wed Mar  7 2007 - simon.zheng@sun.com
- Bump to version 0.994
- Modify %file to enable gimp-plugin
* Sun Nov  5 2006 - laca@sun.com
- Create
