%define src_name orc

Name:		SFEorc
Version:	0.4.4
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
find $RPM_BUILD_ROOT/%{_libdir} -name \*.a -or -name \*.la -delete
rm -rf $RPM_BUILD_ROOT/%{_libdir}/orc


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Apr 09 2010 - Milan Jurik
- initial multiarch support
