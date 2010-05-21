#
# spec file for package SFEopenjpeg
#
# includes module(s): openjpeg
#
%include Solaris.inc

%define	src_name openjpeg
%define	src_url	http://www.openjpeg.org
%define src_version v1_3

Name:                SFEopenjpeg
Summary:             Open Source multimedia framework
Version:             1.3
Source:              http://openjpeg.googlecode.com/files/%{src_name}_%{src_version}.tar.gz
Patch1:		     openjpeg-01-makefile.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %{name}-%{src_version}
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export prefix=%{_prefix}
cd OpenJPEG_%{src_version}
make

%install
rm -rf $RPM_BUILD_ROOT
export prefix=%{_prefix}
cd OpenJPEG_%{src_version}
make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_libdir}
ln -s ./libopenjpeg.so.* ./libopenjpeg.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri May 21 2010 - Milan Jurik
- update to 1.3, split devel package
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
