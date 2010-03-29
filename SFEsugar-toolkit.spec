#
# spec file for package SFEsugar-toolkit
#
# includes module(s): sugar-toolkit
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEsugar-toolkit
Summary:                 Sugar Learning Platform Toolkit
URL:                     http://www.sugarlabs.org/
Version:                 0.87.8
Source:                  http://download.sugarlabs.org/sources/sucrose/glucose/sugar-toolkit/sugar-toolkit-%{version}.tar.bz2
Patch1:                  sugar-toolkit-01-noalsa.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgtk2
Requires:                SUNWgnome-config
Requires:                SUNWgnome-python26-libs
Requires:                SFEhippodraw
Requires:                SFEpython26-telepathy
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWgnome-config-devel
BuildRequires:           SUNWgnome-python26-libs-devel
BuildRequires:           SFEhippodraw-devel
BuildRequires:           SFEpython26-telepathy

%if %build_l10n
%package l10n
Summary:      %{summary} - l10n files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:     %{name}
%endif

%prep
%setup -q -n sugar-toolkit-%version
%patch1 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
aclocal $ACLOCAL_FLAGS -I ./m4
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

# replace the old scripts with script files
%post
%restart_fmri gconf-cache desktop-mime-cache icon-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/sugar
%dir %attr (0755, root, sys) %{_datadir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Wed Mar 10 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.87.8.
* Tue Feb 02 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.87.3.
* Sun Jul 08 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with 0.84.1.
