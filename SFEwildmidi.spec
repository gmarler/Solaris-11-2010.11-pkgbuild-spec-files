#
# spec file for package SFEwildmidi
#
# includes module(s): wildmidi
#
%include Solaris.inc

Name:		SFEwildmidi
Summary:	wildmidi - software MIDI synthesizer
Group:		Audio
Version:	0.2.3.4
License:	LGPLv3
Source:		%{sf_download}/wildmidi/wildmidi-%{version}.tar.gz
Patch1:		wildmidi-01-solaris.diff
Patch2:		wildmidi-02-sunstudio.diff
Patch3:		wildmidi-03-config.diff
URL:		http://wildmidi.sourceforge.net/
SUNW_BaseDir:	%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
BuildRequires: SUNWaudh

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	/
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n wildmidi-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static		\
	    --disable-debug		\
	    --disable-werror		\
	    --disable-profile		\
	    --disable-optimize		\
	    --disable-temps		\
	    --with-oss

make -j$CPUS 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{_libdir}/lib*a

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Dec 26 2010 - Milan Jurik
- bump to 0.2.3.4
* Sat Jan 13 2009 - Milan Jurik
- workaround for missing __FUNCTION__ support
* Thu Dec 11 2008 - trisk@acm.jhu.edu
- Initial spec
