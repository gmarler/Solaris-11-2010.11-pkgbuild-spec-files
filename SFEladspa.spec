#
# spec file for package SFEladspa.spec
#
# includes module(s): ladspa
#
%include Solaris.inc

%define src_name	ladspa_sdk
%define src_url		http://www.ladspa.org/download

Name:                   SFEladspa
Summary:                Linux Audio Developers Simple Plugin API
Version:                1.13
Source:                 %{src_url}/%{src_name}_%{version}.tgz
Patch1:			ladspa-01-solaris.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibms
Requires: SUNWlibms
BuildRequires: SUNWlibC
Requires: SUNWlibC

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -library=Cstd"
export LDFLAGS="%_ldflags"
export bindir=%{_bindir}
export libexecdir=%{_libexecdir}
export includedir=%{_includedir}
cd src
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
export bindir=%{_bindir}
export libexecdir=%{_libexecdir}
export includedir=%{_includedir}
cd src
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sun Aug 09 2009 - Thomas Wagner
- (Build)Requires: SUNWlibms SUNWlibC
* Sun Mar  9 2008 - brian.cameron@sun.com
- Bump to 1.13.
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
