%global priority 59
%global fontname liberation-narrow
%global fontconf %{priority}-%{fontname}.conf
%global catalogue %{_sysconfdir}/X11/fontpath.d

Name:			%{fontname}-fonts
Summary:		Sans-serif Narrow fonts to replace commonly used Microsoft Arial Narrow
Version:			1.07.5
Release:			2%{?dist}
# The license of the Liberation Fonts is a EULA that contains GPLv2 and two
# exceptions:
# The first exception is the standard FSF font exception.
# The second exception is an anti-lockdown clause somewhat like the one in
# GPLv3. This license is Free, but GPLv2 and GPLv3 incompatible.
License:			Liberation
URL:			https://github.com/liberationfonts/liberation-sans-narrow
Source0:		https://github.com/liberationfonts/liberation-sans-narrow/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:		%{name}-generate.pe
Source2:		%{name}.conf
Source3:		%{name}.metainfo.xml
BuildArch:		noarch
BuildRequires:	fontpackages-devel, xorg-x11-font-utils
BuildRequires:	fontforge
BuildRequires:	libappstream-glib
Requires:		fontpackages-filesystem

%description
The Liberation Sans Narrow Fonts are intended to be replacements for \
the Arial Narrow.

%prep
%autosetup %{name}
rm -rf scripts
mv src/LiberationSansNarrow* .
rm -rf src
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .
chmod 755 %{name}-generate.pe

%build
./%{name}-generate.pe *.sfd

%install
# fonts .ttf
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

# catalogue
install -m 0755 -d %{buildroot}%{catalogue}
ln -s %{_fontdir} %{buildroot}%{catalogue}/%{name}

# fonts.{dir,scale}
mkfontscale %{buildroot}%{_fontdir}
mkfontdir %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
		%{buildroot}%{_fontconfig_confdir}
install -m 0644 -p %{SOURCE2} \
		%{buildroot}%{_fontconfig_templatedir}/%{fontconf}
install -Dm 0644 -p %{SOURCE3} \
	%{buildroot}%{_datadir}/metainfo/%{fontname}.metainfo.xml

ln -s %{_fontconfig_templatedir}/%{fontconf} \
		%{buildroot}%{_fontconfig_confdir}/%{fontconf}


%check
appstream-util validate-relax --nonet \
	%{buildroot}%{_datadir}/metainfo/%{fontname}.metainfo.xml

%_font_pkg -f %{fontconf} *.ttf

%doc AUTHORS ChangeLog COPYING README.rst TODO
%license License.txt
%{_datadir}/metainfo/%{fontname}.metainfo.xml
%verify(not md5 size mtime) %{_fontdir}/fonts.dir
%verify(not md5 size mtime) %{_fontdir}/fonts.scale
%{catalogue}/%{name}

%changelog
*Tue Aug 14 2018 Vishal Vijayraghavan <vishalvijayraghavan@gmail.com> - 1.07.5-2
- Resolves: rhbz#1614530

*Mon Jul 23 2018 Vishal Vijayraghavan <vishalvijayraghavan@gmail.com> - 1.07.5-1
- new release since liberation-narrow font is seperted from liberation 1.x

* Fri Nov 23 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-10
- added fontpackages-filesystem in requires

* Thu Nov 22 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-9
- spec file clean up

* Thu Jul 26 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-8
- updated as per pkg review comments #840878

* Tue Jul 17 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-7
- Initial release after splitting it from liberation-fonts tarball due to license incompatibility.
