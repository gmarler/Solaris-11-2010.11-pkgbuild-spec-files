#
# spec file for package SFExz
#
# includes module(s): xz
#

%include Solaris.inc

Name:		SFExz
Version:	4.999.9
Summary:	LZMA utils
URL:		http://tukaani.org/xz
Source:		http://tukaani.org/xz/xz-%{version}beta.tar.bz2

Group:		Applications/Archivers
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%define cc_is_gcc 0

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils were written for POSIX-like systems (GNU/Linux,
*BSDs, etc.), but also work on some not-so-POSIX systems like Windows. XZ Utils
are the successor to LZMA Utils. 

%prep
%setup -q -c -n %{name}-%{version}

%build
cd xz-%{version}beta
CFLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64"
CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64"
export CFLAGS CXXFLAGS
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
	    --disable-static			\
	    --disable-assembler
make

%install
cd xz-%{version}beta
rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR=${RPM_BUILD_ROOT}

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755, root, sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Wed Jun 02 2010 - brian.cameron@oracle.com
- Initial setup.
