%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-resource-retriever
Version:        3.0.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS resource_retriever package

License:        BSD
URL:            http://ros.org/wiki/resource_retriever
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-rolling-ament-index-cpp
Requires:       ros-rolling-ament-index-python
Requires:       ros-rolling-libcurl-vendor
Requires:       ros-rolling-ros-workspace
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  ros-rolling-ament-cmake-gtest
BuildRequires:  ros-rolling-ament-cmake-pytest
BuildRequires:  ros-rolling-ament-cmake-ros
BuildRequires:  ros-rolling-ament-index-cpp
BuildRequires:  ros-rolling-ament-index-python
BuildRequires:  ros-rolling-ament-lint-auto
BuildRequires:  ros-rolling-ament-lint-common
BuildRequires:  ros-rolling-libcurl-vendor
BuildRequires:  ros-rolling-python-cmake-module
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
This package retrieves data from url-format files such as http://, ftp://,
package:// file://, etc., and loads the data into memory. The package:// url for
ros packages is translated into a local file:// url. The resourse retriever was
initially designed to load mesh files into memory, but it can be used for any
type of data. The resource retriever is based on the the libcurl library.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Fri Jan 14 2022 Alejandro Hernandez Cordero <alejandro@openrobotics.org> - 3.0.0-1
- Autogenerated by Bloom

* Tue Apr 06 2021 Alejandro Hernandez <alejandro@osrfoundation.org> - 2.5.0-1
- Autogenerated by Bloom

* Thu Mar 18 2021 Alejandro Hernandez <alejandro@osrfoundation.org> - 2.4.2-1
- Autogenerated by Bloom

* Mon Mar 08 2021 Alejandro Hernandez <alejandro@osrfoundation.org> - 2.4.1-1
- Autogenerated by Bloom

