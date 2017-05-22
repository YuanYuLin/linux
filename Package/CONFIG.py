import ops
import iopc

def MAIN_ENV(args):
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    tarball = ops.path_join(pkg_path, "linux-4.3.tar.xz")
    def_config = ops.path_join(pkg_path, "default.config")
    build_dir = ops.path_join(output_dir, "linux-4.3")

    ops.exportEnv(ops.setEnv("linux_tarball", tarball))
    ops.exportEnv(ops.setEnv("linux_build_dir", build_dir))
    ops.exportEnv(ops.setEnv("linux_def_config", def_config))

    return False

def MAIN_EXTRACT(args):
    output_dir = args["output_path"]
    tarball = ops.getEnv("linux_tarball")
    ops.unTarXz(tarball, output_dir)
    return True

def MAIN_CONFIGURE(args):
    def_config = ops.getEnv("linux_def_config")
    build_dir = ops.getEnv("linux_build_dir")
    ops.copyto(def_config, build_dir + "/.config")
    return True

def MAIN_BUILD(args):
    build_dir = ops.getEnv("linux_build_dir")

    extra_conf = []
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    iopc.make(build_dir, extra_conf)

    extra_conf = []
    extra_conf.append("modules")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    iopc.make(build_dir, extra_conf)
    return False

def MAIN_INSTALL(args):
    build_dir = ops.getEnv("linux_build_dir")
    output_dir = args["output_path"]
    '''
    extra_conf = []
    extra_conf.append("modules_install")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("INSTALL_MOD_PATH=" + output_dir)
    iopc.make(build_dir, extra_conf)

    extra_conf = []
    extra_conf.append("firmware_install")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("INSTALL_MOD_PATH=" + output_dir)
    iopc.make(build_dir, extra_conf)
    '''
    return False

def MAIN_CLEAN_BUILD(args):
    output_dir = args["output_path"]
    return False

def MAIN(args):
    print "linux kernel"

