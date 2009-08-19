#
# NoCopyright 2009 - Gilles Dauphin 
#
#

%include Solaris.inc

Name:		SFElzma
Version:	4.32.7
Summary:	LZMA utils
URL:		http://tukaani.org/lzma
Source:		http://tukaani.org/lzma/lzma-%{version}.tar.gz

Group:		Applications/Archivers
License:	GPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%define cc_is_gcc 0

%description
LZMA provides very high compression ratio and fast decompression. The
core of the LZMA utils is Igor Pavlov's LZMA SDK containing the actual
LZMA encoder/decoder. LZMA utils add a few scripts which provide
gzip-like command line interface and a couple of other LZMA related
tools. 


%prep
%setup -q -c -n %{name}-%{version}

%build
cd lzma-%{version}
CFLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64"
CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64"
export CFLAGS CXXFLAGS
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
	    --disable-static
make

%install
cd lzma-%{version}
rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR=${RPM_BUILD_ROOT}

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
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Aug 2009 - Gilles Dauphin
- Initial setup.
