Name:           objectweb-asm-commons
Version:        7.1
Release:        2
Summary:        Class adapters based on ASM, a Java bytecode manipulation framework
License:        BSD
URL:            https://asm.ow2.org/
BuildArch:      noarch
BuildRequires:	jdk-current
BuildRequires:	javapackages-local
BuildRequires:	jmod(org.objectweb.asm)
BuildRequires:	jmod(org.objectweb.asm.tree)

Source0:        https://repository.ow2.org/nexus/content/repositories/releases/org/ow2/asm/asm-commons/%{version}/asm-commons-%{version}-sources.jar
Source1:        https://repository.ow2.org/nexus/content/repositories/releases/org/ow2/asm/asm-commons/%{version}/asm-commons-%{version}.pom

%description
Useful class adapters based on ASM, a very small and fast Java
bytecode manipulation framework

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
This package provides %{summary}.

%prep
%autosetup -p1 -c asm-commons-%{version}

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

cat >module-info.java <<'EOF'
module org.objectweb.asm.commons {
	exports org.objectweb.asm.commons;
	requires org.objectweb.asm;
	requires org.objectweb.asm.tree;
}
EOF
find . -name "*.java" |xargs javac -p %{_javadir}/modules
javadoc -d docs -sourcepath . org.objectweb.asm.commons -p %{_javadir}/modules
find . -name "*.java" |xargs rm -f
jar cf asm-commons-%{version}.jar META-INF org module-info.class
cp %{S:1} .

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp asm-commons-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap asm-commons-%{version}.pom asm-commons-%{version}.jar
cp -a docs %{buildroot}%{_javadocdir}/org.objectweb.asm.commons
mv %{buildroot}%{_javadir}/*.jar %{buildroot}%{_javadir}/modules/
ln -s modules/asm-commons-%{version}.jar %{buildroot}%{_javadir}/
ln -s modules/asm-commons-%{version}.jar %{buildroot}%{_javadir}/asm-commons.jar
ln -s modules/asm-commons-%{version}.jar %{buildroot}%{_javadir}/org.objectweb.asm.commons.jar

%files -f .mfiles
%{_javadir}/*.jar
%{_javadir}/modules/*.jar

%files javadoc
%{_javadocdir}/org.objectweb.asm.commons
