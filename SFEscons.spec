#
# spec file for package SFEscons
#
# includes module(s): SCons
#

%include Solaris.inc
Name:                    SFEscons
Summary:                 SCons - a software construction tool
Version:                 1.2.0
URL:                     http://www.scons.org/
Source:                  %{sf_download}/scons/scons-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
BuildRequires:           SUNWPython-devel

%include default-depend.inc

%prep
%setup -q -n scons-%version

%build
python setup.py build \
    --build-base=$RPM_BUILD_ROOT%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix $RPM_BUILD_ROOT%{_prefix}

mkdir $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_datadir} 

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/scons-*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*

%changelog
* Sat Feb 21 2009 - sobotkap@gmail.com
- Bump to 1.2.0
* Sat Sep 13 2008 - sobotkap@gmail.com
- Bump to 1.01
* Wed May 23 2007 - nonsea@users.sourceforge.net
- Bump to 0.97
* Tue Mar 06 2007 - nonsea@users.sourceforge.net
- Initial spec file
