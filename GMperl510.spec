#
# spec file for package:  GMperl510
#
#
%include Solaris.inc

Name:             GMperl510
Summary:          Practical Extraction and Report Language
Version:          5.10.1
License:          Artistic
Source:           http://www.cpan.org/src/perl-%{version}.tar.gz
Patch1:           perl-%{version}-change-inc.patch
SUNW_BaseDir:     %{_basedir}
SUNW_Copyright:   %{name}.copyright
BuildRoot:        %{_tmppath}/%{name}-%{version}-build

# The prefix matches the one that Sun/Oracle has used for deployment over
# the years, and prevents any kind of collision with existing versions
%ifarch sparc
%define perl_arch_dir sun4-solaris-64int
%else
%define perl_arch_dir i86pc-solaris-64int 
%endif
%define           vendor          GM
%define           perl5_dir       %{_prefix}/perl5
%define           perl_prefix     %{perl5_dir}/%{version}
%define           perl_lib        %{perl_prefix}/lib
%define           perl_archlib    %{perl_lib}/%{perl_arch_dir}
%define           perl_mandir     %{perl_prefix}/man
%define           perl_sitedir    %{perl5_dir}/site_perl
%define           perl_sitelib    %{perl_sitedir}/%{version}
%define           perl_sitearch   %{perl_sitelib}/%{perl_arch_dir}
%define           perl_vendordir  %{perl5_dir}/vendor_perl
%define           perl_vendorlib  %{perl_vendordir}/%{version}/%{vendor}
%define           perl_vendorarch %{perl_vendordir}/%{version}/%{vendor}/%{perl_arch_dir}


%include default-depend.inc

Requires:         SFEbdb

BuildRequires:    SFEbdb
BuildRequires:    SUNWgmake

%description
Perl is a general-purpose programming language originally developed for 
text manipulation and now used for a wide range of tasks including
system administration, web development, network programming, GUI 
development, and more.

The language is intended to be practical (easy to use, efficient,
complete) rather than beautiful (tiny, elegant, minimal).  Its major
features are that it's easy to use, supports both procedural and 
object-oriented (OO) programming, has powerful built-in support for text
processing, and has one of the world's most impressive collections of
third-party modules.

%clean
rm -rf $RPM_BUILD_ROOT

%prep
rm -rf perl-%{version}
%setup -q -n perl-%{version}
%patch1 -p1

%build
CPUS=$(/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' ')
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CONFIGURE_ENV=""

export INC_COMPAT="5.8.0 5.8.2 5.8.4 5.8.6 5.8.7 5.8.8 5.10.0"
# export PERL_LIBS="-lsocket -lnsl -lgdbm -ldb-4.8 -ldl -lm -lpthread -lc -lperl"
export PERL_LIBS="-lsocket -lnsl -ldb-4.8 -ldl -lm -lpthread -lc"

export CFLAGS="%optflags -I%{_prefix}/gnu/include"
export LDFLAGS="%_ldflags -L%{_prefix}/gnu/lib -R%{_prefix}/gnu/lib -L%{_libdir} -R%{_libdir}"


# Configure Perl
# $CONFIGURE_ENV ./Configure             \
./Configure                             \
  -Darchlib=%{perl_archlib}             \
  -Dcc="$CC"                            \
  -Dccflags="$CFLAGS"                   \
  -Dccversion="%{CC_VERSION}"           \
  -Dcf_email="root@bloomberg.net"       \
  -Dinc_version_list="$INC_COMPAT"      \
  -Dld="$CC"                            \
  -Dldflags="$LDFLAGS"                  \
  -Dlibperl=libperl.so.%{version}       \
  -Dlocincpth=%{includedir}             \
  -Dloclibpth=%{_libdir}                \
  -Dman1dir=%{perl_mandir}/man1         \
  -Dman1ext=1                           \
  -Dman3dir=%{perl_mandir}/man3         \
  -Dman3ext=3perl                       \
  -Doptimize="%{optflags}"              \
  -Dperladmin="root@localhost"          \
  -Dprefix=%{perl_prefix}               \
  -Dprivlib=%{perl_lib}                 \
  -Dsitearch=%{perl_sitearch}           \
  -Dsitelib=%{perl_sitelib}             \
  -Dsiteman1dir=%{perl_mandir}/man1     \
  -Dsiteman3dir=%{perl_mandir}/man3     \
  -Dsiteprefix=%{perl_prefix}           \
  -Duselargefiles                       \
  -Duseshrplib                          \
  -Dusesitecustomize                    \
  -Dusethreads                          \
  -Dccdlflags="-R %{perl_archlib}/CORE" \
  -Dvendorarch=%{perl_vendorarch}/%{vendor} \
  -Dvendorlib=%{perl_vendorlib}/%{vendor}   \
  -Dvendorprefix=%{perl_prefix}         \
  -Dlibs="$PERL_LIBS"                   \
  -Dlibsdirs=" /usr/lib "               \
  -Dsed=%{_bindir}/gsed                 \
  -des

gmake regen_headers
gmake -j$CPUS

# This takes a while...
# gmake test

%install
gmake DESTDIR=$RPM_BUILD_ROOT install

%clean

%files
%defattr (-,root,bin)
%dir %attr(-,root,bin)
/usr/perl5/%{version}/*
%dir %attr(-,root,bin)
/usr/perl5/site_perl/*

%changelog

