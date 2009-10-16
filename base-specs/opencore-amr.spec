#
# spec file for package SFEopencore-amr
#
# includes module(s): opencore-amr
#

%define src_name opencore-amr

Name:		SFEopencore-amr
Summary:	OpenCORE AMR speech codec library
Version:	0.1.2
URL:		http://opencore-amr.sourceforge.net/
License:	Apache License 2.0
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-build

%description
Library of OpenCORE Framework implementation of Adaptive Multi Rate Narrowband and Wideband speech codec.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir}	\
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared		\
            --disable-compile-c

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun Oct 16 2009 - Milan Jurik
- Initial spec
