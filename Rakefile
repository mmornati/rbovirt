# Rakefile to build a project using HUDSON

begin
  require 'rdoc/task'
rescue LoadError
  require 'rake/rdoctask'
end

require 'rake/packagetask'
require 'rake/clean'
require 'find'
require 'rake/gempackagetask'

PROJ_DOC_TITLE = "rbovirt"
PROJ_VERSION = "0.0.15"
PROJ_RELEASE = "1"
PROJ_NAME = "rbovirt"
PROJ_RPM_NAMES = [PROJ_NAME]
PROJ_FILES = ["lib", "spec", "doc"]
RDOC_EXCLUDES = []

ENV["RPM_VERSION"] ? CURRENT_VERSION = ENV["RPM_VERSION"] : CURRENT_VERSION = PROJ_VERSION
ENV["BUILD_NUMBER"] ? CURRENT_RELEASE = ENV["BUILD_NUMBER"] : CURRENT_RELEASE = PROJ_RELEASE
ENV["DEB_DISTRIBUTION"] ? PKG_DEB_DISTRIBUTION = ENV["DEB_DISTRIBUTION"] : PKG_DEB_DISTRIBUTION = "unstable"

CLEAN.include(["build", "doc", "rpm-build"])

def announce(msg='')
  STDERR.puts "================"
  STDERR.puts msg
  STDERR.puts "================"
end

def init
      #FileUtils.mkdir("build") unless File.exist?("build")
end

def safe_system *args
  raise RuntimeError, "Failed: #{args.join(' ')}" unless system *args
end

spec = Gem::Specification.new do |s|
  s.name = "rbovirt"
  s.version = PROJ_VERSION
  s.authors = ["Amos Benari"]

  s.homepage = "http://github.com/rbovirt/rbovirt"
  s.summary = %Q{A Ruby client for oVirt REST API}
  s.description = %Q{A Ruby client for oVirt REST API}
  s.files = FileList["{lib}/**/*"].to_a
  s.require_path = "lib"
  s.has_rdoc = true

  excluded_files = []

  excluded_files.each do |file|
    s.files.delete_if {|f| f.match(/^#{file}/)}
  end
end

Rake::GemPackageTask.new(spec) do |pkg|
  pkg.need_tar = false
  pkg.need_zip = false
  pkg.package_dir = "build"
end

desc "Build documentation, tar balls and rpms"
task :default => [:package]

# task for building docs
rd = Rake::RDocTask.new(:doc) { |rdoc|
  rdoc.rdoc_dir = 'doc'
  rdoc.title    = "#{PROJ_DOC_TITLE} version #{CURRENT_VERSION}"
  rdoc.options << '--line-numbers' << '--main' << 'rbovirt'

  RDOC_EXCLUDES.each do |ext|
    rdoc.options << '--exclude' << ext
  end
}

desc "Run spec tests"
task :test do
    sh "cd spec;rake"
end

desc "Create a tarball for this release"
task :package => [:clean, :doc] do
  announce "Creating rubygem-#{PROJ_NAME}-#{CURRENT_VERSION}.tgz"

  FileUtils.mkdir_p("build/rubygem-#{PROJ_NAME}")
  safe_system("cp -R #{PROJ_FILES.join(' ')} build/rubygem-#{PROJ_NAME}")

  safe_system("cd build && tar --exclude .git -cvzf #{PROJ_NAME}-#{CURRENT_VERSION}.tgz rubygem-#{PROJ_NAME}")
end

desc "Creates a RPM"
task :rpm => [:package] do
  announce("Building RPM for #{PROJ_NAME}-#{CURRENT_VERSION}-#{CURRENT_RELEASE}")

    
  rpmdefines = ""
  topdir = File.expand_path(File.dirname(__FILE__)) + "/rpm-build"

  rpmdefines << " --define \"_topdir #{topdir}\""
  rpmdefines << " --define \"_builddir #{topdir}\""
  rpmdefines << " --define \"_rpmdir #{topdir}\""
  rpmdefines << " --define \"_srcrpmdir #{topdir}\""
  rpmdefines << " --define \"_specdir #{topdir}\""
  rpmdefines << " --define \"_sourcedir  #{topdir}\""

  #sourcedir = `rpm --eval '%_sourcedir'`.chomp
  #specsdir = `rpm --eval '%_specdir'`.chomp
  #srpmsdir = `rpm --eval '%_srcrpmdir'`.chomp
  #rpmdir = `rpm --eval '%_rpmdir'`.chomp
  lsbdistrel = `lsb_release -r -s | cut -d . -f1`.chomp
  lsbdistro = `lsb_release -i -s`.chomp

  `which rpmbuild-md5`
  rpmcmd = $?.success? ? 'rpmbuild-md5' : 'rpmbuild'

  case lsbdistro
  when 'CentOS'
    rpmdist = ".el#{lsbdistrel}"
  when 'Fedora'
    rpmdist = ".fc#{lsbdistrel}"
  else
    rpmdist = ""
  end

  FileUtils.mkdir_p("#{topdir}")
  safe_system %{cp build/#{PROJ_NAME}-#{CURRENT_VERSION}.tgz #{topdir}}
  safe_system %{cp ext/redhat/#{PROJ_NAME}.spec #{topdir}}
  safe_system %{cat ext/redhat/#{PROJ_NAME}.spec|sed -e s/%{rpm_release}/#{CURRENT_RELEASE}/g | sed -e s/%{version}/#{CURRENT_VERSION}/g > #{topdir}/#{PROJ_NAME}.spec}

  if ENV['SIGNED'] == '1'
    safe_system %{#{rpmcmd} #{rpmdefines} --sign -D 'version #{CURRENT_VERSION}' -D 'rpm_release #{CURRENT_RELEASE}' -D 'dist #{rpmdist}' -D 'use_lsb 0' -ba #{topdir}/#{PROJ_NAME}.spec}
  else
    safe_system %{#{rpmcmd} #{rpmdefines} -D 'version #{CURRENT_VERSION}' -D 'rpm_release #{CURRENT_RELEASE}' -D 'dist #{rpmdist}' -D 'use_lsb 0' -ba #{topdir}/#{PROJ_NAME}.spec}
  end

  safe_system %{cp #{topdir}/rubygem-#{PROJ_NAME}-#{CURRENT_VERSION}-#{CURRENT_RELEASE}#{rpmdist}.src.rpm build/}

  safe_system %{cp #{topdir}/*/rubygem-#{PROJ_NAME}*-#{CURRENT_VERSION}-#{CURRENT_RELEASE}#{rpmdist}.*.rpm build/}
  safe_system %{rm -rf #{topdir}}
end

desc "Create the .debs"
task :deb => [:clean, :doc, :package] do
  announce("Building debian packages")

  FileUtils.mkdir_p("build/deb")
  Dir.chdir("build/deb") do
    safe_system %{tar -xzf ../#{PROJ_NAME}-#{CURRENT_VERSION}.tgz}
    safe_system %{cp ../#{PROJ_NAME}-#{CURRENT_VERSION}.tgz #{PROJ_NAME}_#{CURRENT_VERSION}.orig.tar.gz}

    Dir.chdir("#{PROJ_NAME}-#{CURRENT_VERSION}") do
      safe_system %{cp -R ext/debian .}
      safe_system %{cp -R ext/debian/mcollective.init .}
      safe_system %{cp -R ext/Makefile .}

      File.open("debian/changelog", "w") do |f|
        f.puts("mcollective (#{CURRENT_VERSION}-#{CURRENT_RELEASE}) #{PKG_DEB_DISTRIBUTION}; urgency=low")
        f.puts
        f.puts("  * Automated release for #{CURRENT_VERSION}-#{CURRENT_RELEASE} by rake deb")
        f.puts
        f.puts("    See http://marionette-collective.org/releasenotes.html for full details")
        f.puts
        f.puts(" -- The Marionette Collective <mcollective-dev@googlegroups.com>  #{Time.new.strftime('%a, %d %b %Y %H:%M:%S %z')}")
      end

      if ENV['SIGNED'] == '1'
        if ENV['SIGNWITH']
          safe_system %{debuild -i -k#{ENV['SIGNWITH']}}
        else
          safe_system %{debuild -i}
        end
      else
        safe_system %{debuild -i -us -uc}
      end
    end

    safe_system %{cp *.deb *.dsc *.diff.gz *.orig.tar.gz *.changes ..}
  end
end
