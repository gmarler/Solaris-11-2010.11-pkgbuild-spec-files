#
# spec file for package SFEoptipng.spec
#
# includes module(s): optipng
#
%include Solaris.inc

%define src_name	optipng
%define src_url		http://switch.dl.sourceforge.net/%{src_name}

Name:                   SFEoptipng
Summary:                Advanced PNG Format File Optimizer
Version:                0.6.3
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

mv src/scripts/unix.mak.in src/scripts/unix.mak.in.old
sed -e '/^prefix=/s+=.*$+=%{_prefix}+' \
    -e '/^mandir=/s+=.*$+=%{_mandir}+' \
    -e '/^CC.*=/d' -e '/^CFLAGS.*=/d' -e '/^LDFLAGS.*=/d' \
    -e '/^ZLIB.*=/s+=.*$+= -lz+' \
    -e '/^PNGLIB.*=/s+=.*$+= -lpng -lm+' \
    -e '/^PNGLIB.*=/s+=.*$+= -lpng -lm+' \
    -e '/^LIBS.*=/s+\$([PGNZ]*DIR)/++g' \
    -e '/^\$(OPTIPNG):/s+\$(LIBS)+$(PNGXDIR)/$(PNGXLIB)+' \
    -e 's/-I\$([PGNZ]*DIR)//g' \
    -e '/^.(PNGXDIR)..(PNGXLIB):/s/:.*$/:/' \
    src/scripts/unix.mak.in.old > src/scripts/unix.mak.in
./configure

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%changelog
* Thu Oct 29 2009 - matt@greenviolet.net
- Update to 0.6.3
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version
