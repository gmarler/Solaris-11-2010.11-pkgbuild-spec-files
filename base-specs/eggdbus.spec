Name:         eggdbus
Version:      0.6
Release:      1

Group:        System/Libraries
License:      LGPL
URL:          http://cgit.freedesktop.org/~david/eggdbus/
Source:       http://cgit.freedesktop.org/~david/%{name}/snapshot/%{name}-%{version}.zip


%prep
%setup -q


%build
%ifos linux
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

#aclocal $ACLOCAL_FLAGS
#libtoolize --copy --force
#gtkdocize
#autoheader
#automake -a -c -f
#autoconf
./autogen.sh --prefix=%{_prefix} \
		--bindir=%{_bindir} \
		--libdir=%{_libdir} \
		--mandir=%{_mandir} \
		%{gtk_doc_option}
make -j $CPUS


%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'


%clean 
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue Jan 12 2010 - jedy.wang@sun.com
- Initial spec
