#
# spec file for package SFEamrwb
#
# includes module(s): amrwb
#
%include Solaris.inc

%define	src_ver 7.0.0.3
%define	src_name amrwb
%define	src_url	http://ftp.penguin.cz/pub/users/utx/amr

Name:		SFEamrwb
Summary:	3GPP AMR-WB Floating-point Speech Codec
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Source1:	http://www.3gpp.org/ftp/Specs/archive/26_series/26.204/26204-700.zip
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
3GPP AMR-WB Floating-point Speech Codec

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
cp %{SOURCE1} .

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal -I ./m4
autoconf -f
automake -a -f
PATCH=/usr/bin/gpatch ./configure --prefix=%{_prefix}	\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --disable-debug

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sat Apr 11 2009 - Milan Jurik
- update for version 7.0.0.3
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
