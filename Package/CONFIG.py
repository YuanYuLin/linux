import ops
import iopc

pkg_path = ""
output_dir = ""
tarball = ""
src_def_config = ""
dst_def_config = ""
build_dir = ""
initramfs_name = "initramfs.cpio.gz"
initramfs_file = ""

def set_global(args):
    global pkg_path
    global output_dir 
    global tarball
    global src_def_config
    global dst_def_config 
    global build_dir 
    global initramfs_file
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    tarball = ops.path_join(pkg_path, "linux-4.3.tar.xz")
    build_dir = ops.path_join(output_dir, "linux-4.3")
    src_def_config = ops.path_join(pkg_path, "default.config")
    dst_def_config = ops.path_join(build_dir, ".config")
    initramfs_file = ops.path_join(iopc.getOutputRootDir(), initramfs_name)

def MAIN_ENV(args):
    set_global(args)

    return False

def MAIN_EXTRACT(args):
    set_global(args)
    ops.unTarXz(tarball, output_dir)
    #iopc.make_initramfs(iopc.getTargetRootfs(), iopc.getOutputRootFile(""))
    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(build_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    ops.kbuild_config_replace(src_def_config, dst_def_config, "CONFIG_INITRAMFS_SOURCE", initramfs_name)

    return True

def MAIN_BUILD(args):
    set_global(args)

    ops.copyto(initramfs_file, build_dir)

    extra_conf = []
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    iopc.make(build_dir, extra_conf)

    extra_conf = []
    extra_conf.append("modules")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    iopc.make(build_dir, extra_conf)

    '''
    extra_conf = []
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("tarxz-pkg")
    iopc.make(build_dir, extra_conf)
    '''

    return False

def MAIN_INSTALL(args):
    set_global(args)

    ops.copyto(ops.path_join(build_dir, "arch/arm/boot/zImage"), iopc.getOutputRootDir())
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
    set_global(args)

    return False

def MAIN(args):
    set_global(args)
    print "linux kernel"

