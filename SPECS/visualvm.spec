%define shortname  visualvm
%define uniquename io.github.visualvm
%global debug_package %{nil}

Name:             VisualVM
Version:          2.1.4
Release:          1%{?dist}
Summary:          VisualVM is a visual tool integrating commandline JDK tools and lightweight profiling capabilities
License:          GPL-2.0-only WITH Classpath-exception-2.0
URL:              https://visualvm.github.io/
Source0:          https://github.com/oracle/%{shortname}/archive/refs/tags/%{version}.tar.gz
BuildRequires:    libicns-utils

%description
VisualVM is a tool that provides a visual interface for viewing detailed information about Java technology-based
applications (Java applications) while they are running on a Java Virtual Machine (JVM). VisualVM organizes data about
the JVM software that is retrieved by the Java Development Kit (JDK) tools and presents the information in a way that
enables you to quickly view data on multiple Java applications. You can view data on local applications and applications
that are running on remote hosts. You can also capture data about JVM software instances and save the data to your local
system, and view the data later or share the data with others.


%prep
%setup -qn "%{shortname}-%{version}"
# TODO: netbeans could be packaged separately
unzip visualvm/nb124_platform_09022022.zip
mv netbeans visualvm/


%build
cat > %{uniquename}.metainfo.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>%{uniquename}</id>

  <name>%{name}</name>
  <summary>%{summary}</summary>

  <metadata_license>FSFAP</metadata_license>
  <project_license>GPL-2.0-only WITH Classpath-exception-2.0</project_license>

  <description>
    <p>
      VisualVM is a tool that provides a visual interface for viewing detailed information about Java technology-based applications (Java applications) while they are running on a Java Virtual Machine (JVM). VisualVM organizes data about the JVM software that is retrieved by the Java Development Kit (JDK) tools and presents the information in a way that enables you to quickly view data on multiple Java applications. You can view data on local applications and applications that are running on remote hosts. You can also capture data about JVM software instances and save the data to your local system, and view the data later or share the data with others.
    </p>
  </description>

  <content_rating type="oars-1.1" />

  <launchable type="desktop-id">%{uniquename}.desktop</launchable>
  <screenshots>
    <screenshot type="default">
      <image>https://visualvm.github.io/images/visualvm_screenshot_20.png</image>
    </screenshot>
  </screenshots>

  <icon type="stock">%{shortname}</icon>

  <categories>
    <category>Development</category>
    <category>Java</category>
  </categories>

  <provides>
    <binary>%{shortname}</binary>
  </provides>
</component>
EOF

appstreamcli make-desktop-file %{uniquename}.metainfo.xml %{uniquename}.desktop
echo "StartupWMClass=%{name} %{version}" >> %{uniquename}.desktop

# Create the wrapper for /usr/bin
cat >%{shortname}.sh <<EOF
#!/bin/sh
%{_datadir}/%{shortname}/bin/%{shortname} $@
EOF


export JAVA_HOME=$(realpath $(rpm -ql $(rpm -q --whatprovides java-1.8.0-headless) | grep "jre" | head -n1)/..)
cd visualvm
ant build-zip
cd dist
unzip visualvm.zip

cd visualvm/etc
icns2png -x visualvm.icns


%install
# NOT SURE WE NEED ALL OF THESE
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_datadir}/%{shortname} \
         %{buildroot}%{_datadir}/metainfo/ \
         %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/ \
         %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/ \
         %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/ \
         %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/ \
         %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/ \
         %{buildroot}%{_sysconfdir}/profile.d

cp -a visualvm/dist/visualvm/* \
      %{buildroot}%{_datadir}/%{shortname}/

ln -s ../../../../%{shortname}/etc/visualvm_16x16x32.png   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{shortname}.png
ln -s ../../../../%{shortname}/etc/visualvm_32x32x32.png   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{shortname}.png
ln -s ../../../../%{shortname}/etc/visualvm_128x128x32.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{shortname}.png
ln -s ../../../../%{shortname}/etc/visualvm_256x256x32.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{shortname}.png
ln -s ../../../../%{shortname}/etc/visualvm_512x512x32.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{shortname}.png
#ln -s ../../../../%{shortname}/bin/idea.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{shortname}.svg

install -p -m0755 %{shortname}.sh \
                  %{buildroot}%{_bindir}/%{shortname}

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
                     %{uniquename}.desktop

cp %{uniquename}.metainfo.xml %{buildroot}%{_datadir}/metainfo/

%ifnarch x86_64
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/platform/modules/lib/amd64
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/platform/modules/lib/i386
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/platform/modules/lib/x86
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/platform/modules/lib/x86_64
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk15/linux
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk15/linux-amd64
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk16/linux
    rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk16/linux-amd64
%endif

rm -Rf %{buildroot}%{_datadir}/%{shortname}/bin/visualvm.exe
rm -Rf %{buildroot}%{_datadir}/%{shortname}/platform/modules/lib/aarch64*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk15/mac*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk15/solaris*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk15/windows*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk16/linux-aarch64*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk16/linux-arm*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk16/mac*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk16/solaris*
rm -Rf %{buildroot}%{_datadir}/%{shortname}/visualvm/lib/deployed/jdk16/windows*


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{uniquename}.desktop


%files
%{_bindir}/%{shortname}
%{_datadir}/applications/%{uniquename}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{shortname}.png
%{_datadir}/icons/hicolor/32x32/apps/%{shortname}.png
%{_datadir}/icons/hicolor/128x128/apps/%{shortname}.png
%{_datadir}/icons/hicolor/256x256/apps/%{shortname}.png
%{_datadir}/icons/hicolor/512x512/apps/%{shortname}.png
%{_datadir}/metainfo/%{uniquename}.metainfo.xml
%{_datadir}/%{shortname}
%license %{_datadir}/%{shortname}/LICENSE.txt
%license %{_datadir}/%{shortname}/THIRDPARTYLICENSE
