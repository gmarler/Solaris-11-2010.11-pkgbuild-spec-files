
# spec file for package SFElibvanessa-socket
# used by at least SFEperdition pop3/imap proxy

##TODO## check if changing the tarball name "_" to a "-" makes any problems

#note: "_" instead of "-" for later package name
%define src_name vanessa_socket
%define perditionparentversion 1.17.1

%include Solaris.inc

Name:                    SFElibvanessa-socket
Summary:                 vanessa-socket - TCP socket interface library to support perdition imap/pop3 proxy/loadbalancer
URL:                     http://www.vergenet.net/linux/perdition/
Version:                 0.0.7
Source:                  http://www.vergenet.net/linux/perdition/download/%{perditionparentversion}/vanessa_socket-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SUNWlibpopt-devel
BuildRequires: SFElibvanessa-logger
Requires: SUNWlibpopt
Requires: SFElibvanessa-logger

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"

export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --enable-dynamic     \
            --disable-static

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sat Jul 18 2009 - Thomas Wagner
- Initial spec
