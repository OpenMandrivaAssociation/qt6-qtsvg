%define beta beta5
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtsvg
Version:	6.0.0
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
BuildRequires:	%{_lib}Qt6Core-devel
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

%prep
%autosetup -p1 -n qtsvg%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DBUILD_EXAMPLES:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DFEATURE_cxx2a:BOOL=ON \
	-DFEATURE_dynamicgl:BOOL=ON \
	-DFEATURE_ftp:BOOL=ON \
	-DFEATURE_opengl_dynamic:BOOL=ON \
	-DFEATURE_use_lld_linker:BOOL=ON \
	-DFEATURE_xcb_native_painting:BOOL=ON \
	-DFEATURE_openssl:BOOL=ON \
	-DFEATURE_openssl_linked:BOOL=ON \
	-DFEATURE_system_sqlite:BOOL=ON \
	-DINPUT_sqlite=system \
	-DQT_WILL_INSTALL:BOOL=ON \
	-D_OPENGL_LIB_PATH=%{_libdir} \
	-DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
	-DOPENGL_glu_LIBRARY=%{_libdir}/libGLU.so \
	-DOPENGL_glx_LIBRARY=%{_libdir}/libGLX.so \
	-DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so

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
for i in %{buildroot}%{_qtdir}/lib/cmake/*; do
	ln -s ../qt%{major}/lib/cmake/$(basename ${i}) %{buildroot}%{_libdir}/cmake/
done

%files
%{_libdir}/cmake/Qt%{major}BuildInternals
%{_libdir}/cmake/Qt%{major}Gui
%{_libdir}/cmake/Qt%{major}Svg
%{_libdir}/cmake/Qt%{major}SvgWidgets
%{_libdir}/libQt%{major}Svg.so
%{_libdir}/libQt%{major}Svg.so.%{major}*
%{_libdir}/libQt%{major}SvgWidgets.so
%{_libdir}/libQt%{major}SvgWidgets.so.%{major}*
%{_qtdir}/include/QtSvg
%{_qtdir}/include/QtSvgWidgets
%{_qtdir}/lib/cmake/Qt%{major}BuildInternals/StandaloneTests/QtSvgTestsConfig.cmake
%{_qtdir}/lib/cmake/Qt%{major}Svg
%{_qtdir}/lib/cmake/Qt%{major}SvgWidgets
%{_qtdir}/lib/cmake/Qt%{major}Gui/Qt6QSvgIconPlugin*.cmake
%{_qtdir}/lib/cmake/Qt%{major}Gui/Qt6QSvgPlugin*.cmake
%{_qtdir}/lib/libQt%{major}Svg.prl
%{_qtdir}/lib/libQt%{major}Svg.so
%{_qtdir}/lib/libQt%{major}Svg.so.%{major}*
%{_qtdir}/lib/libQt%{major}SvgWidgets.prl
%{_qtdir}/lib/libQt%{major}SvgWidgets.so
%{_qtdir}/lib/libQt%{major}SvgWidgets.so.%{major}*
%{_qtdir}/mkspecs/modules/qt_lib_svg.pri
%{_qtdir}/mkspecs/modules/qt_lib_svg_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_svgwidgets.pri
%{_qtdir}/mkspecs/modules/qt_lib_svgwidgets_private.pri
%{_qtdir}/mkspecs/modules/qt_plugin_qsvg.pri
%{_qtdir}/mkspecs/modules/qt_plugin_qsvgicon.pri
%{_qtdir}/modules/Svg.json
%{_qtdir}/modules/SvgWidgets.json
%{_qtdir}/plugins/iconengines/libqsvgicon.so
%{_qtdir}/plugins/imageformats/libqsvg.so
