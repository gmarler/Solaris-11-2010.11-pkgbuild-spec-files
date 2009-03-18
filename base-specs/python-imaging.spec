#
# base spec file for package python-imaging
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%define name python-%oname

Name:                    python-imaging
Summary:                 Python's own image processing library
URL:                     http://www.pythonware.com/products/pil/
Version:                 1.1.6
Source:                  http://effbot.org/downloads/Imaging-%{version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                Python

%{?!pythonver:%define pythonver 2.4}

%prep
%setup -n Imaging-%{version}

%build
perl -pi -e 'print "#!/usr/bin/python%{pythonver}\n" if ( $. == 1 )' Scripts/pilfont.py
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install -O1 --skip-build --root="$RPM_BUILD_ROOT" --prefix="%{_prefix}"

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

echo deleting pyo files
find $RPM_BUILD_ROOT -name '*.pyo' -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files-other
* Thu Nov 27 2008 - darren.kenny@sun.com
- Split from SUNWpython-imaging.spec
* Tue Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Wed May 14 2008 - darren.kenny@sun.com
- Add SUWNjpg dependency.
* Fri Feb 15 2008 - dermot.mccluskey@sun.com
- remove *.pyo
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version
