%global poppler_version 0.24.0
%global glib2_version 2.36.0
%global gtk3_version 3.16.0
%global gxps_version 0.2.1

Name:           evince
Version:        3.22.1
Release:        5.2%{?dist}
Summary:        Document viewer

License:        GPLv2+ and GPLv3+ and LGPLv2+ and MIT and Afmparse
URL:            https://wiki.gnome.org/Apps/Evince
Source0:        https://download.gnome.org/sources/%{name}/3.22/%{name}-%{version}.tar.xz

Patch0:         evince-3.21.4-NPNVToolKit.patch
#https://bugzilla.gnome.org/show_bug.cgi?id=692552
Patch1:         0001-gnome-692552-don-t-complain-about-inability-to-copy-.patch
#https://bugzilla.gnome.org/show_bug.cgi?id=777082
Patch2:         0001-Resolves-rhbz-1404656-crash-on-opening-second-evince.patch
#https://bugzilla.gnome.org/show_bug.cgi?id=766749
Patch3:         0001-Resolves-deb-762530-rhbz-1061177-add-man-pages.patch
Patch4:         0001-Resolves-rhbz-1358249-page-up-down.patch
Patch5:         0001-Revert-Bump-poppler-requirements-to-0.33.0.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1468488
# https://bugzilla.redhat.com/show_bug.cgi?id=1469528
Patch6:         0001-comics-Remove-support-for-tar-and-tar-like-commands.patch

BuildRequires:  pkgconfig(adwaita-icon-theme)
BuildRequires:  pkgconfig(gio-unix-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-x11-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libspectre)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(poppler-glib) >= %{poppler_version}
BuildRequires:  libtiff-devel
BuildRequires:  gettext
BuildRequires:  libtool
BuildRequires:  gtk-doc
BuildRequires:  yelp-tools
BuildRequires:  intltool
BuildRequires:  /usr/bin/desktop-file-validate
BuildRequires:  libappstream-glib
BuildRequires:  gnome-common
# for the nautilus properties page
BuildRequires:  pkgconfig(libnautilus-extension)
# for the dvi backend
BuildRequires:  kpathsea-devel
%if 0%{?fedora}
# for the djvu backend
BuildRequires:  djvulibre-devel
%endif
# for the xps backend
BuildRequires:  pkgconfig(libgxps) >= %{gxps_version}

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}

%description
Evince is simple multi-page document viewer. It can display and print
Portable Document Format (PDF), PostScript (PS) and Encapsulated PostScript
(EPS) files. When supported by the document format, evince allows searching
for text, copying text to the clipboard, hypertext navigation,
table-of-contents bookmarks and editing of forms.

 Support for other document formats such as DVI and DJVU can be added by
installing additional backends.


%package libs
Summary: Libraries for the evince document viewer
%if 0%{?fedora}
Recommends: %{name}-djvu%{?_isa} = %{version}-%{release}
%endif

%description libs
This package contains shared libraries needed for evince


%package devel
Summary: Support for developing backends for the evince document viewer
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files needed for evince
backend development.


%package dvi
Summary: Evince backend for dvi files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: texlive-collection-fontsrecommended

%description dvi
This package contains a backend to let evince display dvi files.


%if 0%{?fedora}
%package djvu
Summary: Evince backend for djvu files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description djvu
This package contains a backend to let evince display djvu files.
%endif

%package nautilus
Summary: Evince extension for nautilus
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: nautilus%{?_isa}

%description nautilus
This package contains the evince extension for the nautilus file manager.
It adds an additional tab called "Document" to the file properties dialog.


%package browser-plugin
Summary: Evince web browser plugin
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: mozilla-filesystem

%description browser-plugin
This package contains the evince web browser plugin.


%prep
%setup -q
%patch0 -p1 -b .NPNVToolKit
%patch1 -p1 -b .gnome-692552
%patch2 -p1 -b .rhbz-1404656
%patch3 -p1 -b .deb-762530-rhbz
%patch4 -p1 -b .rhbz-1358249-page-up-down
%patch5 -p1 -b .poppler-requirements
%patch6 -p1 -b .no-tar

%build
autoreconf -f -i
%configure \
        --disable-static \
        --enable-introspection \
        --enable-comics=yes \
        --enable-dvi=yes \
        --enable-libgnome-desktop \
%if 0%{?fedora}
        --enable-djvu=yes \
%endif
        --enable-xps=yes \
        --enable-t1lib=no
make %{?_smp_mflags} V=1 LIBTOOL=/usr/bin/libtool

%install
%make_install

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/appdata/evince.appdata.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/evince/a.png 

%find_lang evince --with-gnome

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
# Get rid of static libs and .la files.
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/evince/4/backends/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/evince/4/backends/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/evince.desktop

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%post libs -p /sbin/ldconfig

%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null ||:

%postun libs -p /sbin/ldconfig

%files -f evince.lang
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/appdata/evince.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/evince-previewer.desktop
%{_datadir}/icons/hicolor/*/apps/evince.*
%{_datadir}/icons/hicolor/*/apps/evince-symbolic.svg
%{_mandir}/man1/*.1*
%{_libexecdir}/evinced
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service
%{_datadir}/glib-2.0/schemas/org.gnome.Evince.gschema.xml
%{_datadir}/GConf/gsettings/evince.convert
%{_datadir}/thumbnailers/evince.thumbnailer
%{_userunitdir}/evince.service

%files libs
%doc README NEWS AUTHORS
%license COPYING
%{_libdir}/libevview3.so.*
%{_libdir}/libevdocument3.so.*
%dir %{_libdir}/evince
%dir %{_libdir}/evince/4
%dir %{_libdir}/evince/4/backends
%{_libdir}/evince/4/backends/libpdfdocument.so
%{_libdir}/evince/4/backends/pdfdocument.evince-backend
%{_datadir}/appdata/evince-pdfdocument.metainfo.xml

%{_libdir}/evince/4/backends/libpsdocument.so
%{_libdir}/evince/4/backends/psdocument.evince-backend
%{_datadir}/appdata/evince-psdocument.metainfo.xml

%{_libdir}/evince/4/backends/libtiffdocument.so
%{_libdir}/evince/4/backends/tiffdocument.evince-backend
%{_datadir}/appdata/evince-tiffdocument.metainfo.xml

%{_libdir}/evince/4/backends/libcomicsdocument.so
%{_libdir}/evince/4/backends/comicsdocument.evince-backend
%{_datadir}/appdata/evince-comicsdocument.metainfo.xml

%{_libdir}/evince/4/backends/libxpsdocument.so
%{_libdir}/evince/4/backends/xpsdocument.evince-backend
%{_datadir}/appdata/evince-xpsdocument.metainfo.xml

%{_libdir}/girepository-1.0/EvinceDocument-3.0.typelib
%{_libdir}/girepository-1.0/EvinceView-3.0.typelib

%files devel
%{_datadir}/gtk-doc/html/evince/
%{_datadir}/gtk-doc/html/libevview-3.0
%{_datadir}/gtk-doc/html/libevdocument-3.0
%dir %{_includedir}/evince
%{_includedir}/evince/3.0
%{_libdir}/libevview3.so
%{_libdir}/libevdocument3.so
%{_libdir}/pkgconfig/evince-view-3.0.pc
%{_libdir}/pkgconfig/evince-document-3.0.pc
%{_datadir}/gir-1.0/EvinceDocument-3.0.gir
%{_datadir}/gir-1.0/EvinceView-3.0.gir

%files dvi
%{_libdir}/evince/4/backends/libdvidocument.so*
%{_libdir}/evince/4/backends/dvidocument.evince-backend
%{_datadir}/appdata/evince-dvidocument.metainfo.xml

%if 0%{?fedora}
%files djvu
%{_libdir}/evince/4/backends/libdjvudocument.so
%{_libdir}/evince/4/backends/djvudocument.evince-backend
%{_datadir}/appdata/evince-djvudocument.metainfo.xml
%endif

%files nautilus
%{_libdir}/nautilus/extensions-3.0/libevince-properties-page.so

%files browser-plugin
%{_libdir}/mozilla/plugins/libevbrowserplugin.so

%changelog
* Mon Jul 17 2017 Caolán McNamara <caolanm@redhat.com> - 3.22.1-5.2
- Related: #1469528 ensure .desktop file is still valid

* Fri Jul 07 2017 Bastien Nocera <bnocera@redhat.com> - 3.22.1-5.1
+ Fix arbitrary code execution via filename in tar-compressed
  comics archive
- Resolves: #1469528

* Mon Jan 16 2017 Caolán McNamara <caolanm@redhat.com> - 3.22.1-5
- Resolves: rhbz#1358249 restore ctrl page up/down shortcuts

* Tue Jan 10 2017 Caolán McNamara <caolanm@redhat.com> - 3.22.1-4
- Resolves: rhbz#1061177 add man pages for evince-previewer and evince-thumbnailer

* Tue Jan 10 2017 Caolán McNamara <caolanm@redhat.com> - 3.22.1-3
- Resolves: rhbz#1404656 crash on opening second evince window

* Fri Dec 09 2016 Caolán McNamara <caolanm@redhat.com> - 3.22.1-2
- Resolves: rhbz#1022649 don't complain about inability to copy metadata

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0
- Don't set group tags
- Use make_install macro

* Wed Sep 14 2016 Marek Kasik <mkasik@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Mon Aug 15 2016 Marek Kasik <mkasik@redhat.com> - 3.21.4-2
- Check version of NPNVToolkit provided by browser
- Resolves: #1198229

* Wed Jul 20 2016 Richard Hughes <rhughes@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Tue Jun 21 2016 Marek Kasik <mkasik@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Mon Jun 20 2016 Michael Catanzaro <mcatanzaro@gnome.org> - 3.20.0-2
- Remove downstream patch that's no longer needed

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Mar 16 2016 Kalev Lember <klember@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Tue Mar  8 2016 Marek Kasik <mkasik@redhat.com> - 3.18.2-5
- Recognize multipage DjVu MIME type
- Resolves: #1308628

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Marek Kasik <mkasik@redhat.com> - 3.18.2-3
- Fix selection of text on Wayland

* Thu Nov 19 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 3.18.2-2
- Fix installation of symbolic app icon

* Wed Nov 11 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Fri Oct 23 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Fri Oct  9 2015 Marek Kasik <mkasik@redhat.com> - 3.18.0-2
- Recommend evince-djvu in evince-libs not in evince

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Wed Sep 16 2015 Kalev Lember <klember@redhat.com> - 3.17.92-1
- Update to 3.17.92
- Use desktop-file-validate instead of desktop-file-install

* Wed Sep 02 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 3.17.4-3
- Don't recommend nautilus subpackage; it depends on nautilus.

* Wed Sep 02 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 3.17.4-2
- The main package now recommends the djvu and nautilus subpackages.

* Tue Jul 21 2015 David King <amigadave@amigadave.com> - 3.17.4-1
- Update to 3.17.4
- Update URL
- Use pkgconfig for BuildRequires
- Use license for COPYING
- Update man page glob in files section

* Wed Jun 24 2015 Martin Hatina <mhatina@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Mon Jun 22 2015 Martin Hatina <mhatina@redhat.com> - 3.17.2-3
- Avoid crash after reloading document
- Related: #1203277

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Marek Kasik <mkasik@redhat.com> - 3.17.2-1
- Update to 3.17.2

* Thu Apr 30 2015 Marek Kasik <mkasik@redhat.com> - 3.17.1-1
- Update to 3.17.1

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 3.16.0-2
- Use better AppData screenshots

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Marek Kasik <mkasik@redhat.com> - 3.15.92-1
- Update to 3.15.92

* Mon Mar 16 2015 Marek Kasik <mkasik@redhat.com> - 3.15.90-3
- Fix crashes caused by corrupted documents
- Related: #1201996

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.15.90-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 19 2015 Marek Kasik <mkasik@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Wed Jan 21 2015 Marek Kasik <mkasik@redhat.com> - 3.15.4-2
- Revert fix of centering of documents when printing with a manual scale.
- This caused problems with printing of landscape documents.
- Resolves: #1173832

* Tue Jan 20 2015 Marek Kasik <mkasik@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Mon Dec 08 2014 Adam Jackson <ajax@redhat.com> 3.14.1-8
- Don't link against t1lib, freetype is sufficient (#852489)

* Wed Nov 19 2014 Marek Kasik <mkasik@redhat.com> - 3.14.1-7
- Fix configuration with ligbnome-desktop
- Related: #1147270

* Wed Nov 19 2014 Marek Kasik <mkasik@redhat.com> - 3.14.1-6
- Scroll to page on which is the search result selected by user
- when not in continuous mode.
- Resolves: #1162254

* Tue Nov 18 2014 Marek Kasik <mkasik@redhat.com> - 3.14.1-5
- Use libgnome-desktop to generate and cache thumbnails
- Resolves: #1147270

* Wed Nov 12 2014 Richard Hughes <richard@hughsie.com> - 3.14.1-4
- Fix non-Fedora build

* Wed Nov  5 2014 Marek Kasik <mkasik@redhat.com> - 3.14.1-3
- Fix runtime critical warning when starting in fullscreen mode

* Wed Nov  5 2014 Marek Kasik <mkasik@redhat.com> - 3.14.1-2
- Disable toggle-find action for documents not supporting find
- Resolves: #1160376

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92
- Set minimum required glib2 and gtk3 versions

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Fri Aug 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-2
- Split out evince-browser-plugin subpackage

* Sat Aug 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90
- Include new web browser plugin

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3.1-3
- Rebuilt for gobject-introspection 1.41.4

* Wed Jul 09 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3.1-2
- Install application appdata in the main package, not -libs

* Thu Jun 26 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3.1-1
- Update to 3.13.3.1

* Wed Jun 25 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-2
- Drop gnome-icon-theme-symbolic dependency

* Tue Apr 15 2014 Marek Kasik <mkasik@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Mon Apr 14 2014 Marek Kasik <mkasik@redhat.com> - 3.12.0-2
- Don't crash when trying to save a copy
- Resolves: #1086944

* Tue Mar 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Marek Kasik <mkasik@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Sun Feb 23 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Thu Dec 19 2013 Marek Kasik <mkasik@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 18 2013 Marek Kasik <mkasik@redhat.com> - 3.11.1-3
- Fix source URL

* Thu Nov 14 2013 Marek Kasik <mkasik@redhat.com> - 3.11.1-2
- Fix a typo in description of nautilus subpackage
- Resolves: #1028161

* Wed Oct 30 2013 Marek Kasik <mkasik@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 3.9.4-3
- Add requirement of gnome-icon-theme-symbolic
- Resolves: #980751

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Richard Hughes <rhughes@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Wed Jun 19 2013 Marek Kasik <mkasik@redhat.com> - 3.9.3-3
- Require gnome-icon-theme-devel instead of gnome-icon-theme

* Wed Jun 19 2013 Marek Kasik <mkasik@redhat.com> - 3.9.3-2
- Fix changelog dates

* Wed Jun 19 2013 Marek Kasik <mkasik@redhat.com> - 3.9.3-1
- Update to 3.9.3

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2

* Wed May 15 2013 Marek Kasik <mkasik@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Thu Apr 11 2013 Marek Kasik <mkasik@redhat.com> - 3.8.0-3
- Fix a typo and add a description of an option to man page

* Tue Mar 26 2013 Marek Kasik <mkasik@redhat.com> - 3.8.0-2
- Don't remove the NoDisplay key from evince.desktop because
- it has been already removed
- Related: gnome#634245

* Tue Mar 26 2013 Marek Kasik <mkasik@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Thu Mar 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.92-1
- Update to 3.7.92

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-2
- Tighten subpackage deps

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-1
- Update to 3.7.5

* Thu Jan 17 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.7.4-2
- Rebuilt for new libarchive

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Wed Nov 14 2012 Marek Kasik <mkasik@redhat.com> - 3.7.1-3
- Add requirements of texlive-collection-fontsrecommended for evince-dvi
- Related: #843524

* Mon Nov  5 2012 Marek Kasik <mkasik@redhat.com> - 3.7.1-2
- Update License field

* Tue Oct 23 2012 Marek Kasik <mkasik@redhat.com> - 3.7.1-1
- Update to 3.7.1

* Mon Oct 15 2012 Marek Kasik <mkasik@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Sun Oct  7 2012 Jindrich Novy <jnovy@redhat.com> - 3.6.0-2
- rebuild against new kpathsea in TeX Live 2012

* Tue Sep 25 2012 Marek Kasik <mkasik@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Marek Kasik <mkasik@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Wed Aug  8 2012 Marek Kasik <mkasik@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Marek Kasik <mkasik@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Thu Jun 28 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.3-2
- Fix the build by backporting a GIR generation fix

* Wed Jun 27 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Wed Jun  6 2012 Marek Kasik <mkasik@redhat.com> - 3.5.2-1
- Update to 3.5.2

* Wed May 16 2012 Marek Kasik <mkasik@redhat.com> - 3.4.0-3
- Rebuild (poppler-0.20.0)

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-2
- Silence glib-compile-schemas output

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Richard Hughes <rhughes@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Wed Feb 22 2012 Marek Kasik <mkasik@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Tue Feb  7 2012 Marek Kasik <mkasik@redhat.com> - 3.3.5-1
- Update to 3.3.5
- Remove evince-t1font-mapping.patch (committed upstream)
- Solve build issues by running autogen.sh

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.3.4-2
- Rebuilt for new libarchive

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.3.3.1-3
- Really enable XPS support, drop obsolete build options.

* Fri Dec 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3.1-2
- Enable xps support

* Thu Dec 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3.1-1
- Update to 3.3.3.1

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Nov 23 2011 Marek Kasik <mkasik@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 3.2.1-3
- rebuild(poppler)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Marek Kasik <mkasik@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 3.2.0-2
- Rebuild (poppler-0.18.0)

* Tue Sep 27 2011 Marek Kasik <mkasik@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 3.1.90-2
- Rebuild (poppler-0.17.3)

* Tue Aug 30 2011 Marek Kasik <mkasik@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 3.1.2-2
- Rebuild (poppler-0.17.0)

* Thu Jun 16 2011 Marek Kasik <mkasik@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Mon Apr  4 2011 Matthias clasne <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Fri Mar 25 2011 Matthias clasne <mclasen@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Tue Mar 22 2011 Marek Kasik <mkasik@redhat.com> - 2.91.92-2
- Bump release

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 2.91.90-2
- Rebuild (poppler-0.16.3)

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-3
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Mon Jan 24 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-3
- Remove NoDisplay (gnome bug #634245)

* Wed Jan 12 2011 Marek Kasik <mkasik@redhat.com> - 2.91.5-2
- Remove evince-CVE-2010-2640_CVE-2010-2641_CVE-2010-2642_CVE-2010-2643.patch
- Change the way thumbnailer is integrated with system

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Thu Jan  6 2011 Marek Kasik <mkasik@redhat.com> - 2.91.3-6
- Fixes CVE-2010-2640, CVE-2010-2641, CVE-2010-2642 and CVE-2010-2643
- Resolves: #667573

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.91.3-5
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.91.3-4
- rebuild (poppler)

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-3
- Rebuild

* Wed Dec  1 2010 Marek Kasik <mkasik@redhat.com> - 2.91.3-2
- Really update to 2.91.3

* Wed Dec  1 2010 Marek Kasik <mkasik@redhat.com> - 2.91.3-1
- Update to 2.91.3
- Remove evince-page-range.patch

* Mon Nov 22 2010 Marek Kasik <mkasik@redhat.com> - 2.91.2-2
- Fix crash in clear_job_selection()
- Remove unused patches
- Resolves: #647689

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Sat Nov 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.91.1-5.gitf615894
- rebuilt (poppler)

* Fri Nov  5 2010 Marek Kasik <mkasik@redhat.com> - 2.91.1-4.gitf615894
- Rebuild against newer libxml2

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1-gitf615894
- Rebuild against newer gtk3

* Tue Oct 26 2010 Marek Kasik <mkasik@redhat.com> - 2.91.1-1
- Update to 2.91.1
- Remove evince-2.91.0-introspection-build-fix.patch
- Add evince-2.91.1-requires.patch

* Mon Oct 4 2010 Owen Taylor <otaylor@redhat.com> - 2.91.0-1
- Update to 2.91.0 so we can rebuild against current gtk3

* Fri Oct  1 2010 Marek Kasik <mkasik@redhat.com> - 2.32.0-2
- Rebuild against newer poppler

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.92-5
- Fix build against newer gtk

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.92-4
- Rebuild against newer gobject-introspection

* Mon Sep 13 2010 Marek Kasik <mkasik@redhat.com> - 2.31.92-3
- Fix file attributes for nautilus files

* Mon Sep 13 2010 Marek Kasik <mkasik@redhat.com> - 2.31.92-2
- Make "Shrink to Printable Area" option default in "Page Scaling"
- Resolves: #633265

* Mon Sep 13 2010 Marek Kasik <mkasik@redhat.com> - 2.31.92-1
- Update to 2.31.92

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.31.6-2
- rebuild (poppler)

* Mon Aug  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Wed Jul 21 2010 Marek Kasik <mkasik@redhat.com> - 2.31.5-5
- Don't sigsegv when a page is manually entered
- Remove 0001-pdf-Fix-build-when-text_layout-is-not-available.patch

* Fri Jul 16 2010 Marek Kasik <mkasik@redhat.com> - 2.31.5-4
- Restore io mode when returning from opening of synctex file
- Patch by David Tardon
- Resolves: #613916

* Fri Jul 16 2010 Marek Kasik <mkasik@redhat.com> - 2.31.5-3
- Move %%doc files to evince-libs subpackage
-   see Subpackage Licensing in Packaging:LicensingGuidelines

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.31.5-2
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5
- Enable introspection

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.4-1
- Update to 2.31.4

* Mon Jun 28 2010 Marek Kasik <mkasik@redhat.com> - 2.31.3-5.20100621git
- Don't try to install evince.schemas file (it doesn't exist anymore)
- Remove unused patches
- Resolves: #595217

* Mon Jun 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-4.20100621git
- git snapshot that builds against GLib 2.25.9

* Mon Jun 21 2010 Marek Kasik <mkasik@redhat.com> - 2.31.3-3
- Rename gdk_drag_context_get_action to gdk_drag_context_get_selected_action

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-2
- Rebuild against new poppler

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-3
- Migrate settings to dconf

* Sun May 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-2
- Compile GSettings schemas

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Thu Apr 29 2010 Marek Kasik <mkasik@redhat.com> - 2.30.1-2
- Make sure dot_dir exists before creating last_settings file
- backported from upstream
- Related: #586343

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Fri Apr  2 2010 Marek Kasik <mkasik@redhat.com> - 2.30.0-6
- rpmlint related changes:
-   Don't define RPATH
-   Remove static libs
-   Avoid expansion of some macros in changelog

* Fri Apr  2 2010 Marek Kasik <mkasik@redhat.com> - 2.30.0-5
- Update required versions of libraries
- Remove unused patches

* Thu Apr  1 2010 Christoph Wickert <cwickert@fedoraproject.org> - 2.30.0-4
- Update scriptlets
- Make build verbose

* Thu Apr  1 2010 Christoph Wickert <cwickert@fedoraproject.org> - 2.30.0-3
- Split out libevince-properties-page.so into nautilus subpackage
- Resolves: #576435

* Thu Apr  1 2010 Marek Kasik <mkasik@redhat.com> - 2.30.0-2
- Remove deprecated configure flag "--with-print"

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Wed Mar 10 2010 Marek Kasik <mkasik@redhat.com> - 2.29.91-3
- Replace deprecated gtk functions with their equivalents
- Remove unused patches

* Tue Mar  9 2010 Marek Kasik <mkasik@redhat.com> - 2.29.91-2
- Use Type 1 fonts when viewing DVI files
- Use correct name when the font is mapped
- Related: #562648

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.5-2
- Add missing libs

* Tue Jan 12 2010 Marek Kasik <mkasik@redhat.com> - 2.29.5-1
- Update to 2.29.5

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.29.4-1
- Update to 2.29.4

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-1
- Update to 2.29.3

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Sat May 23 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.27.1-2
- Include /usr/include/evince directory (#483306).
- Don't run /sbin/ldconfig in post scriptlet (no shared libs in that pkg).
- Let -libs post/postun run /sbin/ldconfig directly.

* Tue May 19 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Fri May 01 2009 Peter Robinson <pbrobinson@gmail.com> - 2.26.1-1
- Update to 2.26.1

* Fri May 01 2009 Peter Robinson <pbrobinson@gmail.com> - 2.26.0-2
- Split libs out to a subpackage - RHBZ 480729

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Tue Jan 20 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Sat Jan 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 2.25.4-2
- Rebuild with mew djvulibre

* Mon Jan  5 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.4-1
- Update to 2.25.4
- Temporarily drop the duplex patch, it needs updating

* Wed Dec  3 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.2-2
- Update to 2.25.2

* Fri Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.1-5
- Better URL

* Fri Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.1-4
- Tweak %%summary and %%description

* Tue Nov 11 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.1-3
- Update to 2.25.1

* Sat Oct 25 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-3
- Require dbus-glib-devel, not just dbus-devel (#465281, Dan Winship)

* Sat Oct 25 2008 Ville Skyttä <ville.skytta@iki.fi> - 2.24.1-2
- Drop dependency on desktop-file-utils (#463048).

* Mon Oct 20 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Fri Sep  12 2008 Marek Kasik <mkasik@redhat.com> - 2.23.92-2
- fix duplex printing of copies
- upstream bug #455759

* Tue Sep  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.23.6-2
- Include %%_libdir/evince directory.

* Wed Aug  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.4-2
- fix license tag

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Tue Apr  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1.1-1
- Update to 2.22.1.1 (fix link handling in djvu backend)

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Tue Apr  1 2008 Kristian Høgsberg <krh@redhat.com> - 2.22.0-4
- Rebuild against latest poppler.

* Mon Mar 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-3
- Handle all schemas files

* Thu Mar 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Rebuild against the latest poppler

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Mar  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-2
- Rebuild

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Sat Feb  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-5
- Fix nautilus property page and thumbnailer

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-4
- Use libspectre

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-3
- Don't link the thumbnailer against djvu

* Mon Jan 28 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-2
- Rebuild against split poppler

* Mon Jan 28 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Sun Dec 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-2
- Build nautilus extension against nautilus 2.21

* Wed Dec  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Tue Dec  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.2-2
- Enable the dvi backend

* Tue Nov 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.2-1
- Update to 2.20.2

* Mon Nov 26 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-5
- Fix a problem in the tiff patch
- Turn off the dvi backend for now, since the tetex kpathsea 
  gives linker errors on x86_64

* Sat Nov 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-4
- Enable the dvi and djvu backends

* Thu Nov 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-3
- Fix rendering of tiff images (#385671)

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-2
- Rebuild against new dbus-glib

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (bug fixes and translation updates)

* Wed Oct  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-3
- Drop the nautilus dependency (#201967)

* Mon Sep 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Add a missing schema file

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep  4 2007 Kristian Høgsberg <krh@redhat.com> - 2.19.92-1
- Update to 2.19.92.  Evince now follows GNOME version numbers.

* Wed Aug 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.3-5
- Rebuild

* Sat Aug 11 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.3-4
- Fix the build

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.3-3
- Update licence field again
- Use %%find_lang for help files, too
- Add some missing requires

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.3-2
- Update the license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.3-1
- Update to 0.9.3

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Mon Jun 11 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.0-3
- Add comics-related build fixes

* Mon Jun 11 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.0-2
- Enable comics support (#186865)

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Tue Apr  3 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-5
- Add an explicit --vendor="", to pacify older desktop-file-utils

* Sun Apr  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-4
- Add an explicit BR for gnome-icon-theme (#234780)

* Sun Apr  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-3
- Add an explicit --with-print=gtk to configure 
- Drop libgnomeprintui22 BR

* Sat Mar 31 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-2
- Add support for xdg-user-dirs

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1
- Update to 0.8.0
- Use desktop-file-install

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Sun Dec 10 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.1-2
- Fix an overflow in the PostScript backend (#217674, CVE-2006-5864)

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.0-4
- Fix scripts according to the packaging guidelines
 
* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.6.0-3.fc6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.0-2.fc6
- Fix a deadlock in printing

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.0-1.fc6
- Update to 0.6.0

* Mon Aug 21 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.5-2.fc6
- Rebuild agains new dbus.

* Fri Aug 11 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.5-1.fc6
- Update to 0.5.5

* Tue Jul 25 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-3
- Don't ship an icon cache file

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-2
- Rebuild against new dbus

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.4-1.1
- rebuild

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-1
- Update to 0.5.4

* Thu Jun 29 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.3-4
- Bump gtk2 dependency to 2.9.4.

* Thu Jun  8 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.3-3
- Rebuild

* Tue May 30 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.3-2
- Add gettext build requires.

* Mon May 22 2006 Kristian Høgsberg <krh@redhat.com> 0.5.3-1
- Bump poppler_version to 0.5.2.
- Package icons and add %%post and %%postun script to update icon cache.

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.2-1
- update to 0.5.2

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0.5.1-3
- quiet scriptlet spew from gconfd killing

* Wed Mar  1 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.1-2
- Rebuild to pick up new poppler soname.

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.1-1
- Update to 0.5.1
- Drop upstreamed patch

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Christopher Aillon <caillon@redhat.com> 0.5.0-3
- Don't explicitly set the invisible char to '*'

* Mon Jan 23 2006 Kristian Høgsberg <krh@redhat.com> 0.5.0-2
- Spec file update from Brian Pepple <bdpepple@ameritech.net> (#123527):
  - Drop Requires for gtk2 & poppler, devel soname pulls these in.
  - Disable GConf schema install in install section.
  - Add BR for gnome-doc-utils, nautilus & libXt-devel.
  - Use smp_mflags.
  - Drop BR for desktop-file-utils,gcc & gcc-c++.
  - Add URL & full source.
  - Use more macros.
  - Fix ownership of some directories.
  - Drop depreciated prereq, and use requires.
  - Use fedora extras preferred buildroot.
  - Various formatting changes.

* Fri Jan 20 2006 Kristian Høgsberg <krh@redhat.com> 0.5.0-1
- Update to 0.5.0 release.

* Tue Dec 13 2005 Kristian Høgsberg <krh@redhat.com> 0.4.0-4
- Added a couple of missing build requires.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0.4.0-3.1
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-3
- rebuild for new dbus

* Tue Sep 13 2005 Marco Pesenti Gritti <mpg@redhat.com> 0.4.0-2
- Rebuild

* Fri Aug 26 2005 Marco Pesenti Gritti <mpg@redhat.com> 0.4.0-1
- Update to 0.4.0
- No more need to remove ev-application-service.h

* Fri Aug 19 2005 Kristian Høgsberg <krh@redhat.com> 0.3.4-2
- Remove stale autogenerated ev-application-service.h.

* Wed Aug 17 2005 Kristian Høgsberg <krh@redhat.com> 0.3.4-1
- New upstream version again.
- Add nautilus property page .so's.
- Stop scrollkeeper from doing what it does.

* Wed Aug 17 2005 Kristian Høgsberg <krh@redhat.com> 0.3.3-2
- Bump release and rebuild.
- Require poppler > 0.4.0.

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- Newer upstream version

* Tue Aug 09 2005 Andrew Overholt <overholt@redhat.com> 0.3.2-3
- Add necessary build requirements.
- Bump poppler_version to 0.3.3.

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Newer upstream version

* Mon Jun  6 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.1-2
- Add poppler version dep and refactor the gtk2 one

* Sun May 22 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Sat May  7 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.0-1
- Update to 0.3.0

* Sat Apr 23 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.2.1-1
- Update to 0.2.1
- Add help support

* Wed Apr  6 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Sat Mar 12 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.9-1
- Update to 0.1.9

* Sat Mar 12 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Tue Mar  8 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.7-1
- Update to 0.1.7
- Install the new schemas

* Tue Mar  8 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.6-1
- Update to 0.1.6
- Add poppler dependency

* Thu Mar  3 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.5-2
- Rebuild

* Sat Feb 26 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Wed Feb  9 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.4-1
- Update to 0.1.4
- Install schemas and update desktop database

* Fri Feb  4 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.3-1
- Update to 0.1.3

* Tue Feb  1 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Wed Jan 26 2005 Jeremy Katz <katzj@redhat.com> - 0.1.1-1
- 0.1.1

* Thu Jan 20 2005 Jeremy Katz <katzj@redhat.com> - 0.1.0-0.20050120
- update to current cvs

* Thu Jan  6 2005 Jeremy Katz <katzj@redhat.com> - 0.1.0-0.20050106.1
- require gtk2 >= 2.6

* Thu Jan  6 2005 Jeremy Katz <katzj@redhat.com>
- Initial build.
- Add a desktop file
