%define src_name orc

Name:		SFEorc
Version:	0.4.5
Summary:	The Oil Run-time Compiler

Group:		System Environment/Libraries
License:	BSD
URL:		http://code.entropywave.com/projects/orc/
Source:		http://code.entropywave.com/download/orc/orc-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n %{src_name}-%{version}

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export LDFLAGS="$LDFLAGS -m64"
fi

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}                 \
            --datadir=%{_datadir}               \
            --disable-static --enable-gtk-doc

make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove unneeded files.
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/orc


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Jun 18 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 0.4.5.
* Sun Apr 11 2010 - Milan Jurik
- do not depend on GNU find
* Fri Apr 09 2010 - Milan Jurik
- initial multiarch support
