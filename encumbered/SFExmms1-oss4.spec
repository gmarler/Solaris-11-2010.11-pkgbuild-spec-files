#
# spec file for package SFExmms1-oss4
#

%include Solaris.inc

%define longname xmms-OSS4-v

Name:                SFExmms1-oss4
Summary:             OSS4 output plugin for XMMS
Version:             0.10
Source:              http://pkgsrc.sartek.net/pkgz/xmms-OSS4-v%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFExmms1
BuildRequires: SFExmms1

%prep
rm -rf %longname%version
%setup -q -n %longname%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

perl -pi -e 's/-Wall//g' Makefile.*

./configure \
        --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/xmms/Output/libOSS4.la
rm ${RPM_BUILD_ROOT}%{_libdir}/xmms/Output/libOSS4.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/xmms/Output/


%changelog
* Fri Apr 24 2009 - andras.barna@gmail.com
- Initial spec.
