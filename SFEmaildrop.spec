#
# spec file for package SFEmaildrop
#
# includes module(s): maildrop
#
%include Solaris.inc

Name:                    SFEmaildrop
Summary:                 maildrop - mail delivery agent with filtering capabilities
Version:                 2.3.0
License:                 GPLv2
Source:                  %{sf_download}/courier/files/maildrop/%{version}/maildrop-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgamin-devel
Requires: SUNWgamin
Requires: SUNWpcre
Requires: SUNWlibC
Requires: SUNWlibms

%prep
%setup -q -n maildrop-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir}	\
	    --mandir=%{_mandir}		\
	    --without-db		\
	    --enable-smallmsg=65536	\
	    --enable-use-dotlock=1	\
	    --enable-use-flock=1	\
	    --enable-keep-fromline=1	\
	    --disable-authlib		\
	    --enable-maildirquota
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_docdir}
mv $RPM_BUILD_ROOT/%{_datadir}/maildrop/html $RPM_BUILD_ROOT/%{_docdir}/maildrop
rmdir $RPM_BUILD_ROOT/%{_libdir}
rmdir $RPM_BUILD_ROOT/%{_includedir}
rmdir $RPM_BUILD_ROOT/%{_datadir}/maildrop
rmdir $RPM_BUILD_ROOT/%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/lockmail
%{_bindir}/reformime
%{_bindir}/makemime
%{_bindir}/maildirmake
%{_bindir}/reformail
%{_bindir}/deliverquota
%{_bindir}/mailbot
%attr (6755, root, mail) %{_bindir}/maildrop
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/maildrop/*


%changelog
* Tue Feb 04 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
