#
# spec file for package SUNWpython26-coherence
#
# includes module(s): coherence
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define pythonver 2.6
%define src_url         http://coherence.beebits.net/download
%define src_name        Coherence

%use coherence = coherence.spec

Name:                   SUNWpython26-coherence
Summary:                DLNA/UPnP framework for the digital living
URL:                    %{coherence.url}
Version:                %{coherence.version}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython
BuildRequires:          SUNWPython-devel
BuildRequires:          SUNWpython-setuptools

%prep
rm -rf %name-%version
mkdir -p %name-%version
%coherence.prep -d %name-%version

%build
export PYTHON="/usr/bin/python%{pythonver}"
export CFLAGS="%optflags -I/usr/xpg4/include -I%{_includedir} -I/usr/include/python%{pythonver}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
export PYCC_CC="$CC"
export PYCC_CXX="$CXX"
%coherence.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%coherence.install -d %name-%version

# remove coherence for python2.6 package
#rm -rf $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_bindir}/coherence $RPM_BUILD_ROOT%{_bindir}/coherence2.6

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages

%changelog
* Fri Mar 06 2009 - alfred.peng@sun.com
- Create SFEpython24-coherence.spec and coherence.spec to replace
  SFEcoherence.spec.
* Mon Mar 02 2009 - alfred.peng@sun.com
- Bump to 0.6.2. Remove the upstream patch path-blank.diff.
* Mon Feb 16 2009 - alfred.peng@sun.com
- Add patch path-blank.diff to fix packaging problem.
  Bump to 0.6.0.
* Thu Oct 09 2008 - jijun.yu@sun.com
- Initial version.
