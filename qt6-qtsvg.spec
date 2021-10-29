#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

%define libcore %mklibname Qt%{major}Svg %{major}
%define devcore %mklibname -d Qt%{major}Svg
%define libwidgets %mklibname Qt%{major}SvgWidgets %{major}
%define devwidgets %mklibname -d Qt%{major}SvgWidgets

Name:		qt6-qtsvg
Version:	6.2.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtsvg-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtsvg-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Tools
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt6Core-devel >= %{version}-0
BuildRequires:	%{_lib}Qt6Gui-devel
BuildRequires:	%{_lib}Qt6Widgets-devel
BuildRequires:	%{_lib}Qt6Xml-devel
BuildRequires:	%{_lib}Qt6Qml-devel
BuildRequires:	%{_lib}Qt6OpenGL-devel
BuildRequires:	qt%{major}-cmake
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(OpenGL)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} SVG library

%package -n %{libcore}
Summary:	Qt %{major} SVG rendering library
Group:		System/Libraries

%description -n %{libcore}
Qt %{major} SVG rendering library

%package -n %{devcore}
Summary:	Development files for the Qt %{major} SVG rendering library
Group:		System/Libraries
Requires:	%{libcore} = %{EVRD}

%description -n %{devcore}
Development files for the Qt %{major} SVG rendering library

%package -n %{libwidgets}
Summary:	Qt %{major} SVG rendering library
Group:		System/Libraries

%description -n %{libwidgets}
Qt %{major} SVG rendering library

%package -n %{devwidgets}
Summary:	Development files for the Qt %{major} SVG rendering library
Group:		System/Libraries
Requires:	%{libwidgets} = %{EVRD}

%description -n %{devwidgets}
Development files for the Qt %{major} SVG rendering library

%package examples
Summary:	Example code for the Qt 6 SVG module
Group:		Documentation

%description examples
Example code for the Qt 6 SVG module

%prep
%autosetup -p1 -n qtsvg%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
# Static helper lib without headers -- useless
rm -f %{buildroot}%{_libdir}/qt6/%{_lib}/libpnp_basictools.a
# Put stuff where tools will find it
# We can't do the same for %{_includedir} right now because that would
# clash with qt5 (both would want to have /usr/include/QtCore and friends)
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}/cmake
for i in %{buildroot}%{_qtdir}/lib/*.so*; do
	ln -s qt%{major}/lib/$(basename ${i}) %{buildroot}%{_libdir}/
done
mv %{buildroot}%{_qtdir}/lib/cmake %{buildroot}%{_libdir}

%files -n %{libcore}
%{_qtdir}/lib/libQt%{major}Svg.so.%{major}*
%{_libdir}/libQt%{major}Svg.so.%{major}*
%{_qtdir}/plugins/iconengines/libqsvgicon.so
%{_qtdir}/plugins/imageformats/libqsvg.so

%files -n %{devcore}
%{_qtdir}/include/QtSvg
%{_qtdir}/modules/Svg.json
%{_qtdir}/lib/libQt%{major}Svg.prl
%{_qtdir}/lib/libQt%{major}Svg.so
%{_libdir}/libQt%{major}Svg.so
%{_libdir}/cmake/Qt%{major}BuildInternals/StandaloneTests/QtSvgTestsConfig.cmake
%{_libdir}/cmake/Qt%{major}Svg
%{_libdir}/cmake/Qt%{major}Gui/Qt6QSvgIconPlugin*.cmake
%{_libdir}/cmake/Qt%{major}Gui/Qt6QSvgPlugin*.cmake
%{_qtdir}/lib/metatypes/qt6svg_relwithdebinfo_metatypes.json
%{_qtdir}/mkspecs/modules/qt_lib_svg.pri
%{_qtdir}/mkspecs/modules/qt_lib_svg_private.pri

%files -n %{libwidgets}
%{_qtdir}/lib/libQt%{major}SvgWidgets.so.%{major}*
%{_libdir}/libQt%{major}SvgWidgets.so.%{major}*

%files -n %{devwidgets}
%{_qtdir}/include/QtSvgWidgets
%{_qtdir}/modules/SvgWidgets.json
%{_qtdir}/lib/libQt%{major}SvgWidgets.prl
%{_qtdir}/lib/libQt%{major}SvgWidgets.so
%{_libdir}/cmake/Qt%{major}SvgWidgets
%{_libdir}/libQt%{major}SvgWidgets.so
%{_qtdir}/mkspecs/modules/qt_lib_svgwidgets.pri
%{_qtdir}/mkspecs/modules/qt_lib_svgwidgets_private.pri
%{_qtdir}/lib/metatypes/qt6svgwidgets_relwithdebinfo_metatypes.json
   
%files examples
%{_qtdir}/examples
