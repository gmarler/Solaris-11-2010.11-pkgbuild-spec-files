#
# spec file for package SFErrdtool
#

#TODO# python might love a subdirectory "rrdtool" under site-packages:  lib/python2.4/site-packages/rrdtoolmodule.so


%include Solaris.inc

%define src_name rrdtool

#below compare with perl-modules SFEperl-*
%define perl_version 5.8.4

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif

%define SUNWruby18u    %(/usr/bin/pkginfo -q SUNWruby18u && echo 1 || echo 0)
%define SUNWPython     %(/usr/bin/pkginfo -q SUNWPython && echo 1 || echo 0)



Name:                    SFErrdtool
Summary:                 rrdtool - data logging and graphing system for time series data.
URL:                     http://http://oss.oetiker.ch/rrdtool/
Version:                 1.3.6
Source:                  http://oss.oetiker.ch/rrdtool/pub/rrdtool-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#use if they are installed
#ruby
%if %SUNWruby18u
BuildRequires: SUNWruby18u
#user decides at runtime
#Requires: SUNWruby18u
%else
%endif

#python 2.4 (or what rrdtool delivers)
%if %SUNWPython
BuildRequires: SUNWPython-devel
Requires: SUNWPython-devel
#user decides at runtime
#Requires: SUNWPython
%else
%endif

#want perl modules, right.
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584core
BuildRequires:           SUNWsfwhea

#bug and lacks perl modules (, ruby, python too)
Conflicts: SUNWrrdtool

%include default-depend.inc



%prep
%setup -q -n rrdtool-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi


./configure --prefix=%{_prefix}  \
	    --bindir=%{_bindir}  \
            --mandir=%{_mandir}  \
            --libdir=%{_libdir}/%{src_name} \
            --datadir=%{_datadir}	    \
            --libexecdir=%{_libdir}/%{src_name}/bin \
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --with-perl-options="PREFIX=%{_prefix} INSTALLSITELIB=%{_prefix}/perl5/vendor_perl/%{perl_version} INSTALLSITEARCH=%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} INSTALLSITEMAN1DIR=%{_mandir}/man1 INSTALLSITEMAN3DIR=%{_mandir}/man3 INSTALLMAN1DIR=%{_mandir}/man1 INSTALLMAN3DIR=%{_mandir}/man3" \
            --disable-static


            #--with-perl-options="PREFIX=$RPM_BUILD_ROOT%{_prefix} INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3" \

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

[ -f $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int/auto/RRDp/.packlist ] && rm $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int/auto/RRDp/.packlist
[ -f $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int/auto/RRDs/.packlist ] && rm $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int/auto/RRDs/.packlist

#eliminate this one here %{_libdir}/i86pc-solaris-64int/perllocal.pod
[ -d $RPM_BUILD_ROOT%{_libdir}/i86pc-solaris-64int/perllocal.pod ] && rm -rf $RPM_BUILD_ROOT%{_libdir}/i86pc-solaris-64int/

#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README COPYING NEWS TODO THREADS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/*

%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*
#%{_libdir}/%{src_name}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/*
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}-%{version}/*
#%{_docdir}/%{name}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*



%changelog
* Thr Feb 27 2009  - Thomas Wagner
- Initial spec version 1.3.6
- include Perl-Support to "use RRDs/RRDp", ruby, python support
