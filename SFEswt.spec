#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEswt
Summary:             Standard Widget Toolkit
Version:             3.4.2
Source:              http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/eclipse/downloads/drops/R-3.4.2-200902111700/swt-%{version}-gtk-solaris-sparc.zip

#http://www.mirrorservice.org/sites/download.eclipse.org/eclipseMirror/eclipse/downloads/drops/R-3.3.2-200802211800/swt-3.3.2-gtk-solaris-sparc.zip

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n swt-%version

%build

unzip -o src.zip

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

#Check if CDE is available if yes build with support for it.
if [[ -d /usr/dt ]]; then
	make -j$CPUS -f make_solaris.mak CDE_HOME=/usr/dt JAVA_HOME=/usr/java all make_cairo make_gnome
else
	make -j$CPUS -f make_solaris.mak JAVA_HOME=/usr/java make_swt make_atk make_awt make_glx make_cairo make_gnome 
fi

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/swt
cp *.so $RPM_BUILD_ROOT/%{_libdir}/swt
cp *.jar $RPM_BUILD_ROOT/%{_libdir}/swt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/swt
%{_libdir}/swt/*

%changelog
* Mon May 18 2009 - pradhap <at> gmail.com
- Bump up the version, fix URL and if condition
* Sun Oct 12 2008 - sobotkap@gmail.com
- Check if there is installed CDE if not then build without it.
* Fri Jun 20 2008 - river@wikimedia.org
- Initial spec.
