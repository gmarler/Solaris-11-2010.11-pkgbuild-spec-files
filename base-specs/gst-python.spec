#
# base spec file for package gst-python
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%{?!pythonver:%define pythonver 2.4}

Name:                    gst-python
Summary:                 Python bindings for the GStreamer streaming media framework
URL:                     http://gstreamer.freedesktop.org/src/gst-python/
Version:                 0.10.14
Source:                  http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                python
Requires:                gstreamer

%prep
%setup -q -n %name-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
./configure --prefix=%{_prefix}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files
* Tue Mar 03 2009 - brian.cameron@sun.com
- Use find command to remove .la files.
* Mon Jan 19 2009 - brian.cameron@sun.com
- Bump to 0.10.14.
* Mon Nov 24 2008 - laca@sun.com
- split from SUNWgst-python.spec
* Mon Oct 13 2008 - brian.cameron@sun.com
- Bump to 0.10.13.  Remove upstream patch gst-python-01-pipelinetester.diff.
* Fri Sep 12 2008 - matt.keenn@sun.com
- Update copyright
* Wed Jul 16 2008 - damien.carbery@sun.com
- Update %files for newly delivered library.
* Thu Jun 19 2008 - brian.cameron@sun.com
- Bump to 0.10.12.
* Thu Mar 20 2008 - brian.cameron@sun.com
- Bump to 0.10.11.
* Tue Mar 18 2008 - damien.carbery@sun.com
- Add Build/Requires for SUNWgnome-python-libs and SUNWgnome-media.
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version

