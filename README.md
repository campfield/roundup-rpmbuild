# [campfield/roundup_rpmbuild] Roundup Issue Tracker RPM build for EL7 systemd-based systems

# Overview
This repository contains the necessary SPEC and SOURCE files required to build
RPM files for the [Roundup Issue Tracker](http://www.roundup-tracker.org).  This
build is configured for use with EL7+ systems with systemd.

Distributions, including Fedora, have stopped maintaining packages for Roundup
due to the packagers not providing a version compatible with systemd and the
roundup packages are not present in EPEL or similar repository locations.

## Building the package
This package can be built with the standard rpmbuild toolchain and has been built
and tested under CentOS 7.3.

## Configuring and Running Roundup
Consult the /usr/share/doc/roundup-1.5.1/README.linux file for infomation about
configuring and initializing roundup's trackers.

The package installer requires the presence of Apache httpd server but if installed
along with the roundup package, such as through a 'yum localinstall' will not (re)start
or enable the httpd serice for system boot no alter the firewall policies to
allow access to the necessary httpd ports.

## Notes
This package was adapted from files extracted from Fedora Linux source RPM for roundup version:
roundup-1.4.20-1.el6.src.rpm.
