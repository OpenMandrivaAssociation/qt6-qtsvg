#define beta rc

Name:		qt6-qtsvg
Version:	6.6.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}2
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtsvg-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtsvg-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
# Bugfixes from upstream master branch. Generated with
# git format-patch v6.6.0, then picked relevant fixes
# manually...
Patch1:		0018-Build-with-QT_NO_CONTEXTLESS_CONNECT.patch
Patch2:		0019-Build-with-QT_NO_CONTEXTLESS_CONNECT.patch
Patch3:		0029-Support-display-none-for-Graphical-Nodes.patch
Patch7:		0044-Add-Radial-Gradient-default-value.patch
Patch10:	0054-Add-selectable-featureSet-to-all-QSvg-classes.patch
Patch11:	0060-Change-Axivion-configuration.patch
Patch12:	0063-Fix-nullptr-dereference-with-invalid-SVG.patch
Patch13:	0064-Fix-crash-when-reading-text-with-line-breaks.patch
Patch14:	0066-Make-sure-we-don-t-load-invalid-SVGs-twice.patch
Patch15:	0067-Verify-that-loading-of-invalid-SVG-files-don-t-crash.patch
Patch16:	0075-Private-API-for-iterating-over-QSvgTinyDocument.patch
Patch17:	0078-Add-virtual-destructor-to-QSvgVisitor.patch
Patch18:	0081-Refactor-QSvgNode-draw-architecture.patch
Group:		System/Libraries
Summary:	Qt %{qtmajor} Tools
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	qt6-cmake
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(OpenGL)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{qtmajor} SVG library

%define extra_files_Svg \
%{_qtdir}/plugins/iconengines/libqsvgicon.so \
%{_qtdir}/plugins/imageformats/libqsvg.so

%define extra_devel_files_Svg \
%{_qtdir}/lib/cmake/Qt6Gui/Qt6QSvg*.cmake

%qt6libs Svg SvgWidgets

%package examples
Summary:	Example code for the Qt 6 SVG module
Group:		Documentation

%description examples
Example code for the Qt 6 SVG module

%prep
%autosetup -p1 -n qtsvg%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DBUILD_WITH_PCH:BOOL=OFF

#	-DQT_MKSPECS_DIR:FILEPATH=%{_qtdir}/mkspecs \
%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

#files examples
#{_qtdir}/examples
