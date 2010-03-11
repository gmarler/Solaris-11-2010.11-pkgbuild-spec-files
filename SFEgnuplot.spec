#
# spec file for package SFEgnuplot
#
# includes module(s): gnuplot
#
%include Solaris.inc

Name:                    SFEgnuplot
Summary:                 gnuplot
Version:                 4.2.5
Source:			 http://downloads.sourceforge.net/%{summary}/%{summary}-%{version}.tar.gz
Patch1:			gnuplot-01.diff
URL:                     http://www.gnuplot.info
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWpng
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWzlib
Requires: SUNWtexi
Requires: SUNWgd2
#Requires: SUNWwxwidgets
BuildRequires: SUNWpng-devel

%prep
%setup -q -n gnuplot-%version
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS=""
export CFLAGS="-I/usr/include/gd2 -I/usr/gnu/include"
export CPPFLAGS=" -I/usr/include/gd2 -I/usr/gnu/include"
export CXXFLAGS=""
export CXX="${CXX}"

./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
	    --disable-wxwidgets			\
	    --infodir=%{_datadir}/info
	    
make 

%install
# workaround for bug http://defect.opensolaris.org/bz/show_bug.cgi?id=3644
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/X11/app-defaults
mkdir -p $RPM_BUILD_ROOT/usr/X11/lib/app-defaults
#pushd $RPM_BUILD_ROOT/usr/lib
#ln -s ../X11/lib X11
#popd
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir
mv "${RPM_BUILD_ROOT}/usr/lib/X11/app-defaults/Gnuplot" "${RPM_BUILD_ROOT}/usr/X11/lib/app-defaults/"
rm -rf ${RPM_BUILD_ROOT}/usr/lib/X11

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gnuplot.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gnuplot.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr(0755, root, bin) %{_datadir}/emacs
%dir %attr(0755, root, bin) %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*
%dir %attr(0755, root, sys) %{_datadir}/gnuplot
%{_datadir}/gnuplot/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/lib
%dir %attr (0755, root, bin) %{_prefix}/X11/lib/app-defaults
%{_prefix}/X11/lib/app-defaults/*


%changelog
* Jan 28 2010 - Gilles dauphin
- bump to 4.2.5
- workaround /usr/lib/X11 and /usr/X11/lib
* Thu Dec 11 2008 - Gilles dauphin
- bump to 4.2.4
* Jeudi Nov 13 2008 - Gilles dauphin
- In B101 SUNWgd2 and include/gd2
* Tue Oct 23 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Fix links
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency. Add %post/%preun to update the info dir file.
* Fri Jun 30 2006 - laca@sun.com
- rename to SFEgnuplot
- delete -share subpkg
- update file attributes
* Thu Apr  6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Sun Dec  4 2005 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
