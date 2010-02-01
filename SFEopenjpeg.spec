#
# spec file for package SFEopenjpeg
#
# includes module(s): openjpeg
#
%include Solaris.inc

%define	src_name openjpeg
%define	src_url	http://www.openjpeg.org

Name:                SFEopenjpeg
Summary:             Open Source multimedia framework
Version:             v1_2
Source:              %{src_url}/%{src_name}_%{version}.tar.gz
Patch1:		     openjpeg-01-makefile.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n %{name}-%{version}
cd trunk
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export prefix=%{_prefix}
cd trunk
make

%install
rm -rf $RPM_BUILD_ROOT
export prefix=%{_prefix}
cd trunk
make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_libdir}
ln -s ./libopenjpeg.so.* ./libopenjpeg.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}
%{_includedir}

%changelog
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
