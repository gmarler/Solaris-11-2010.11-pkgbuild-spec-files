#
# base spec file for package coherence
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# bugdb: http://coherence.beebits.net/ticket/$bugid
#
%{?!pythonver:%define pythonver 2.4}

%define src_url         http://coherence.beebits.net/download
%define src_name        Coherence

Name:                    Coherence
Summary:                 DLNA/UPnP framework for the digital living
URL:                     http://coherence.beebits.net
Version:                 0.6.2
Source:                  %{src_url}/%{src_name}-%{version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                python

# owner:alfred date:2009-03-06 type:bug bugid=194
Patch1:                  coherence-01-solaris.diff

%prep
%setup -q -n %name-%version
%patch1 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
python%{pythonver} setup.py build

%install
python%{pythonver} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} 

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

# remove applet-coherence which depends on python-qt
rm $RPM_BUILD_ROOT%{_bindir}/applet-coherence

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Mar 06 2009 - alfred.peng@sun.com
- initial version 0.6.2.
