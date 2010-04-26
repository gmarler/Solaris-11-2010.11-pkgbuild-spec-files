#
# spec file for package SFElibantlr3c.spec
#
# includes module(s): libantlr3c
#
%include Solaris.inc

%define src_name	libantlr3c
%define src_url		http://www.antlr.org/download/C

%define SFEdoxygen      %(/usr/bin/pkginfo -q SFEdoxygen && echo 1 || echo 0)
%define FOSSgraphviz    %(/usr/bin/pkginfo -q FOSSgraphviz && echo 1 || echo 0)

Name:                   SFElibantlr3c
Summary:                ANother Tool for Language Recognition C target
Version:                3.2
License:                BSD
URL:                    http://www.antlr.org/wiki/display/ANTLR3/ANTLR3+Code+Generation+-+C
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
This is the C language target for ANTLR.  It requires
ANTLR with the same version number.  Currently the SFEantlr.spec
file is for an obsolete ANTLR version.  Which seems difficult
to fix at the moment, as the ANTLR 3.2 build system using maven
panics during the build as described in the BUILD.txt file included
in the ANTLR v3.2 distribution.  Then the build has to be restarted some
number of times, this makes it difficult to automate the ANTLR 3.2
build with a spec file.  This issue may be fixed eventually
in ANTLR v4, as the intention is to drop the maven build system and
go back to ANT.

%if %SFEdoxygen
%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:      %name
BuildRequires: SFEdoxygen
%if %{FOSSgraphviz}
BuildRequires: FOSSgraphviz
%else
BuildRequires: SFEgraphviz
%endif
%endif

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CPPFLAGS="-D_POSIX_SOURCE -D__EXTENSIONS__ -D_XPG4_2 -DHAVE_NETINET_TCP_H"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --enable-static
make -j$CPUS

%if %{SFEdoxygen}
%if %{FOSSgraphviz}
# Use /opt/kde4/bin/dot from FOSSgraphviz for Solaris 10
export PATH="$PATH:/opt/foss/bin:/opt/kde4/bin"
%endif
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %{SFEdoxygen}
install -d -m 0755 $RPM_BUILD_ROOT/%{_datadir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_docdir}
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/libantlr3c
install -m 644 api/*.html $RPM_BUILD_ROOT%{_docdir}/libantlr3c
install -m 644 api/*.png $RPM_BUILD_ROOT%{_docdir}/libantlr3c
install -d -m 0755 $RPM_BUILD_ROOT%{_mandir}
install -d -m 0755 $RPM_BUILD_ROOT%{_mandir}/man3
install -m 644 api/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}/antlr3.h
%{_includedir}/antlr3baserecognizer.h
%{_includedir}/antlr3basetree.h
%{_includedir}/antlr3basetreeadaptor.h
%{_includedir}/antlr3bitset.h
%{_includedir}/antlr3collections.h
%{_includedir}/antlr3commontoken.h
%{_includedir}/antlr3commontree.h
%{_includedir}/antlr3commontreeadaptor.h
%{_includedir}/antlr3commontreenodestream.h
%{_includedir}/antlr3config.h
%{_includedir}/antlr3convertutf.h
%{_includedir}/antlr3cyclicdfa.h
%{_includedir}/antlr3debugeventlistener.h
%{_includedir}/antlr3defs.h
%{_includedir}/antlr3encodings.h
%{_includedir}/antlr3errors.h
%{_includedir}/antlr3exception.h
%{_includedir}/antlr3filestream.h
%{_includedir}/antlr3input.h
%{_includedir}/antlr3interfaces.h
%{_includedir}/antlr3intstream.h
%{_includedir}/antlr3lexer.h
%{_includedir}/antlr3memory.h
%{_includedir}/antlr3parser.h
%{_includedir}/antlr3parsetree.h
%{_includedir}/antlr3recognizersharedstate.h
%{_includedir}/antlr3rewritestreams.h
%{_includedir}/antlr3string.h
%{_includedir}/antlr3stringstream.h
%{_includedir}/antlr3tokenstream.h
%{_includedir}/antlr3treeparser.h

%{_libdir}/libantlr3c.a
%{_libdir}/libantlr3c.la
%{_libdir}/libantlr3c.so

%if %SFEdoxygen
%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/libantlr3c
%{_docdir}/libantlr3c/*.html
%{_docdir}/libantlr3c/*.png
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%endif

%changelog
* Mon Apr 26 2010 - markwright@internode.on.net
- Initial version
